from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from books_service.models import Book
from borrowings_service.models import Borrowing
from borrowings_service.serializers import BorrowingSerializer


class BorrowingsServiceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@case.test",
            password="test123password"
        )
        self.client.force_authenticate(user=self.user)
        self.book_in_stock = Book.objects.create(
            title="TEST",
            author="TEST",
            inventory=99,
            daily_fee="20.05"
        )
        self.book_out_of_stock = Book.objects.create(
            title="TEST1",
            author="TEST",
            inventory=0,
            daily_fee="20.05"
        )
        self.borrow_date = timezone.now()
        self.valid_return_date = self.borrow_date + timezone.timedelta(days=1)

    def test_return_date_cannot_be_before_borrow_date(self):
        invalid_return_date = self.valid_return_date - timezone.timedelta(days=2)

        borrowing = Borrowing(
            borrow_date=self.borrow_date,
            expected_return_date=invalid_return_date,
            book=self.book_in_stock,
            user=self.user,
        )

        with self.assertRaises(ValidationError):
            borrowing.clean()

    def test_validate_book_in_stock(self):
        borrowing_data = {
            "borrow_date": self.borrow_date,
            "expected_return_date": self.valid_return_date,
            "book": self.book_in_stock.id,
            "user": self.user.id,
        }
        serializer = BorrowingSerializer(data=borrowing_data)
        self.assertTrue(serializer.is_valid())

    def test_validate_book_out_of_stock(self):
        borrowing_data = {
            "borrow_date": self.borrow_date,
            "expected_return_date": self.valid_return_date,
            "book": self.book_out_of_stock.id,
            "user": self.user.id,
        }
        serializer = BorrowingSerializer(data=borrowing_data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("This book is out of stock.", str(context.exception))

    def test_create_borrowing_decrements_inventory(self):
        initial_inventory = self.book_in_stock.inventory

        res = self.client.post(
            reverse("borrowings:borrowing-list"),
            {
                "book": self.book_in_stock.id,
                "expected_return_date": self.valid_return_date
            },
            format="json"
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.book_in_stock.refresh_from_db()
        self.assertEqual(self.book_in_stock.inventory, initial_inventory - 1)
