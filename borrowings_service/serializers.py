from rest_framework import serializers
from books_service.models import Book
from borrowings_service.models import Borrowing
from books_service.serializers import BookSerializer


class BookDetailSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ("title", "author", "cover", "daily_fee")


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookDetailSerializer(many=False, read_only=True)
