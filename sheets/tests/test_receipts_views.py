from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import Http404
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from sheets.models import Expense, Category

class ReceiptViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.client.login(
            username="testuser",
            password="testpass123"
        )

        self.category = Category.objects.create(
            name="Test Category"
        )

    def test_receipts_month_view_returns_200(self):
        response = self.client.get(
            reverse(
                "sheets:receipts_month_view",
                kwargs={"year": 2026, "month": 6}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_receipts_month_view_contains_context(self):
        response = self.client.get(
            reverse(
                "sheets:receipts_month_view",
                kwargs={"year": 2026, "month": 6},
            )
        )

        self.assertIn("receipts", response.context)
        self.assertIn("receipts_count", response.context)
        self.assertEqual(response.context["receipts_count"], 0)
    
    def test_receipts_month_view_receipts_count_is_zero(self):
        response = self.client.get(
            reverse(
                "sheets:receipts_month_view",
                kwargs={"year": 2026, "month": 6},
            )
        )

        self.assertEqual(response.context["receipts_count"], 0)
        self.assertEqual(len(response.context["receipts"]), 0)

    def test_receipt_download_missing_receipt_returns_404(self):
        response = self.client.get(
            reverse(
                "sheets:receipt_download",
                kwargs={"pk": 9999}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_receipt_download_returns_file(self):
        receipt = SimpleUploadedFile(
            "receipt.txt",
            b"test receipt content",
            content_type="text/plain",
        )

        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=10,
            date=datetime.date(2026, 6, 1),
            receipt=receipt,
        )

        response = self.client.get(
            reverse(
                "sheets:receipt_download",
                kwargs={"pk": expense.pk},
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            "attachment",
            response["Content-Disposition"],
        )

    def test_receipts_month_download_no_receipts_returns_404(self):
        response = self.client.get(
            reverse(
                "sheets:receipts_month_download",
                kwargs={"year": 2026, "month": 6},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_receipts_month_download_single_receipt(self):
        receipt = SimpleUploadedFile(
            "receipt.txt",
            b"test receipt content",
            content_type="text/plain",
        )

        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=10,
            date=datetime.date(2026, 6, 1),
            receipt=receipt,
        )

        response = self.client.get(
            reverse(
                "sheets:receipts_month_download",
                kwargs={"year": 2026, "month": 6},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "attachment",
            response["Content-Disposition"],
        )