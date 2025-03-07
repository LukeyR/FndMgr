from django.db.models import Sum
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets

from fund.filters import FundFilter
from fund.forms import CSVUploadForm
from fund.models import Fund, StrategyType
from fund.serializers import FundSerializer, parse_csv


class FundList(viewsets.ModelViewSet):
    queryset = Fund.full_prefetch.all()
    serializer_class = FundSerializer
    filterset_class = FundFilter


def index(request):
    strategy_filter = request.GET.get("strategy")
    funds = Fund.full_prefetch.all()

    if strategy_filter:
        strategy_filter = int(
            strategy_filter
        )  # Even if its id=0, it will be a str
        funds = funds.filter(strategy__id=strategy_filter)

    total_funds_count = funds.count()
    total_aum_sum = funds.aggregate(Sum("amount"))["amount__sum"]

    strategies = StrategyType.objects.filter(funds__isnull=False).distinct()

    context = {
        "funds": funds,
        "strategies": strategies,
        "total_funds_count": total_funds_count,
        "total_aum_sum": total_aum_sum,
        "strategy_filter": strategy_filter,  # Pass current filter for template
    }
    return render(request, "fund/index.html", context)


def csv_upload(request: HttpRequest):

    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            errors = parse_csv(request.FILES["csv_upload"])

            return render(
                request,
                "fund/upload_csv.html",
                {"form": form, "errors": errors},
            )
    else:
        form = CSVUploadForm()
    return render(
        request, "fund/upload_csv.html", {"form": form, "errors": []}
    )
