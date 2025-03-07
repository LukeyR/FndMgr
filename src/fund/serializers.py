import csv
import io
from datetime import datetime, date

from django.core.files.uploadedfile import UploadedFile
from django.db import transaction, connection
from rest_framework import serializers

from fund.models import Fund, StrategyType, FundName


class FundSerializer(serializers.ModelSerializer):
    fund = serializers.CharField(source="fund.name", read_only=True)
    strategy = serializers.CharField(
        source="strategy.description", read_only=True
    )

    class Meta:
        model = Fund
        fields = ["id", "fund", "strategy", "amount", "inception"]


def parse_csv(csv_file: UploadedFile) -> tuple[list[str], int]:
    errors: list[str] = []
    fund_names_to_create: list[FundName] = []
    strategies_to_create: list[StrategyType] = []
    funds_to_create: list[tuple[str, str, float, date]] = []
    total_lines = 0

    try:
        decoded_file = csv_file.read().decode("utf-8")
        # Need to be careful here, big CSV is ready to kill us
        csv_reader = csv.reader(io.StringIO(decoded_file), delimiter="\t")

        __headers = next(csv_reader)

        line_num = 0
        for line_num, row in enumerate(csv_reader, start=1):
            try:
                fund_name_str, strategy_str, amount_str, inception_str = row

                fund_name = FundName(name=fund_name_str)
                strategy = StrategyType(description=strategy_str)
                fund_names_to_create.append(fund_name)
                strategies_to_create.append(strategy)

                amount = float(amount_str)
                inception = datetime.strptime(inception_str, "%Y-%m-%d").date()

                funds_to_create.append(
                    (fund_name_str, strategy_str, amount, inception)
                )

            except ValueError as e:
                errors.append(
                    f"File {csv_file.name} (line: {line_num}): Error parsing entry {e}"
                )
        total_lines = line_num


    except ValueError as e:
        errors.append(f"File {csv_file.name}: Error parsing file {e}")

    with transaction.atomic():
        temp = FundName.objects.bulk_create(
            fund_names_to_create, ignore_conflicts=True
        )
        fund_names_temp = {obj.name for obj in temp}

        temp = StrategyType.objects.bulk_create(
            strategies_to_create, ignore_conflicts=True
        )
        strategies_temp = {obj.description for obj in temp}
        fund_names = {
            obj.name: obj
            for obj in FundName.objects.filter(name__in=fund_names_temp)
        }
        strategies = {
            obj.description: obj
            for obj in StrategyType.objects.filter(
                description__in=strategies_temp
            )
        }

        Fund.objects.bulk_create(
            (
                Fund(
                    fund=fund_names[fund_name],
                    strategy=strategies[strategy],
                    amount=amount,
                    inception=inception,
                )
                for fund_name, strategy, amount, inception in funds_to_create
            ),
            ignore_conflicts=True,
        )

    return errors, total_lines-len(errors)
