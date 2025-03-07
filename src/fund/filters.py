from django.db.models import QuerySet
from django_filters import rest_framework as filters

from fund.models import Fund


class FundFilter(filters.FilterSet):
    strategy = filters.CharFilter(
        field_name="strategy__description", lookup_expr="iexact"
    )

    class Meta:
        model = Fund
        fields = ("strategy",)
