from django.contrib import admin

from fund.models import Fund, FundName, StrategyType


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    pass


@admin.register(FundName)
class FundNameAdmin(admin.ModelAdmin):
    pass


@admin.register(StrategyType)
class StrategyTypeAdmin(admin.ModelAdmin):
    pass
