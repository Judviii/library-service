from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        read_only_fields = ["actual_return_date", "user"]

    def validate_book(self, value):
        if value.inventory <= 0:
            raise ValidationError("This book is out of stock.")
        return value

    @transaction.atomic()
    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory -= 1
        book.save()

        return super().create(validated_data)


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookDetailSerializer(many=False, read_only=True)
