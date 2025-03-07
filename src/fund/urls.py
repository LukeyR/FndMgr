from django.urls import path, include
from rest_framework import routers

from fund.views import FundList, index, csv_upload

router = routers.SimpleRouter()
router.register(r"funds", FundList, "funds")

urlpatterns = [
    path("upload_csv/", csv_upload, name="csv_upload"),
    path("", index, name="fund_list"),
    path("api/", include(router.urls)),
]
