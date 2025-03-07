from datetime import date
from urllib.parse import urlencode

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from fund.models import Fund, FundName, StrategyType
from fund.serializers import parse_csv


class APITestCases(TestCase):
    def setUp(self):

        self.fund_name_1 = FundName.objects.create(name="test1")
        self.fund_name_2 = FundName.objects.create(name="test2")
        self.strategy_type_1 = StrategyType.objects.create(
            description="test_start1"
        )
        self.strategy_type_2 = StrategyType.objects.create(
            description="test_start2"
        )
        self.fund1 = Fund.objects.create(
            fund=self.fund_name_1,
            strategy=self.strategy_type_1,
            amount=1,
            inception=date.today(),
        )
        self.fund2 = Fund.objects.create(
            fund=self.fund_name_2,
            strategy=self.strategy_type_2,
            amount=2,
            inception=date.today(),
        )

    def test_simple_retrieve_all(self):
        response = self.client.get(reverse("funds-list"))
        res_body = response.json()
        self.assertEqual(len(res_body), 2)
        self.assertEqual(res_body[0]["fund"], self.fund_name_1.name)
        self.assertEqual(
            res_body[0]["strategy"], self.strategy_type_1.description
        )
        self.assertEqual(res_body[1]["fund"], self.fund_name_2.name)
        self.assertEqual(
            res_body[1]["strategy"], self.strategy_type_2.description
        )

    def test_simple_retrieve_single(self):
        response = self.client.get(
            reverse("funds-detail", args=[self.fund1.id])
        )
        res_body = response.json()
        self.assertEqual(res_body["fund"], self.fund_name_1.name)
        self.assertEqual(
            res_body["strategy"], self.strategy_type_1.description
        )

    def test_simple_retrieve_filter(self):
        response = self.client.get(
            f"{reverse("funds-list")}?{urlencode({"strategy": self.strategy_type_1.description})}"
        )
        res_body = response.json()
        self.assertEqual(len(res_body), 1)
        self.assertEqual(res_body[0]["fund"], self.fund_name_1.name)
        self.assertEqual(
            res_body[0]["strategy"], self.strategy_type_1.description
        )


class ViewsTestCases(TestCase):
    def test_upload_csv(self):
        csv_data = (
            "Name\tStrategy\tAUM (USD)\tInception Date\n"
            "Test Fund 1\tArbitrage\t1000000\t2023-10-26\n"
            "Test Fund 2\tGlobal Macro\t2000000\t2023-11-15\n"
            "Test Fund 2\tArbitrage\t2000000\t2023-11-15"
        )
        csv_file = SimpleUploadedFile(
            "funds_test.csv", csv_data.encode("utf-8"), content_type="text/csv"
        )
        errors = parse_csv(csv_file)

        self.assertEqual(len(errors), 0)

        self.assertEqual(FundName.objects.all().count(), 2)
        self.assertEqual(StrategyType.objects.all().count(), 2)
        self.assertEqual(Fund.objects.all().count(), 3)
