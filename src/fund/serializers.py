import csv
import io
from datetime import datetime, date

from django.core.files.uploadedfile import UploadedFile
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


def parse_csv(csv_file: UploadedFile) -> list[str]:
    errors: list[str] = []
    fund_names_to_create: list[FundName] = []
    strategies_to_create: list[StrategyType] = []
    funds_to_create: list[tuple[str, str, float, date]] = []

    try:
        decoded_file = csv_file.read().decode("utf-8")
        # Need to be careful here, big CSV is ready to kill us
        csv_reader = csv.reader(io.StringIO(decoded_file), delimiter="\t")

        __headers = next(csv_reader)

        for line_num, row in enumerate(csv_reader, start=1):
            try:
                fund_name_str, strategy_str, amount_str, inception_str = row

                fund_name, _ = FundName.objects.get_or_create(name=fund_name_str)
                strategy, _ = StrategyType.objects.get_or_create(description=strategy_str)

                amount = float(amount_str)
                inception = datetime.strptime(inception_str, "%Y-%m-%d").date()

                Fund.objects.update_or_create( # Is this definitely what we want?
                    fund=fund_name,
                    strategy=strategy,
                    amount=amount,
                    inception=inception,
                )

            except ValueError as e:
                errors.append(
                    f"File {csv_file.name} (line: {line_num}): Error parsing line {e}"
                )

    except ValueError as e:
        errors.append(f"File {csv_file.name}: Error parsing file {e}")

    return errors
