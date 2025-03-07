from django.db import models


class FundName(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return f"FundName ({self.id}): {self.name}"


class StrategyType(models.Model):
    description = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f"StrategyType ({self.id}): {self.description}"


class FundManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("fund", "strategy")


class Fund(models.Model):
    # Opted to split these into separate models
    # I figured a fund can have many strategies (e.g. Long An Equity,
    # Short A different Equity). But also, many funds can have the same
    # "StrategyType" (e.g. 2 firms could be Long an Equity)
    #
    # Other option here was to use an Enum like this
    #
    # class StrategyTypes(models.Choices):
    #     ...
    #
    # if we are certain we are restricting the type of funds we allow
    # tracking, and won't be modifying at all often (also applies to
    # fund names if we don't want to on board new people easily)

    fund = models.ForeignKey(FundName, on_delete=models.PROTECT)
    strategy = models.ForeignKey(
        StrategyType, on_delete=models.PROTECT, related_name="funds"
    )

    amount = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Do we want more for more precise tracking?

    inception = models.DateField()

    objects = models.Manager()
    full_prefetch = FundManager()

    class Meta:
        unique_together = ("fund", "strategy")

    def __str__(self):
        return (
            f"Fund ({self.id}): {self.fund.name}/{self.strategy.description}"
        )
