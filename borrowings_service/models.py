from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError

from books_service.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Borrow date",
    )
    expected_return_date = models.DateTimeField(
        verbose_name="Expected return date",
    )
    actual_return_date = models.DateTimeField(
        verbose_name="Actual return date",
        null=True,
        blank=True,
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} borrowed {self.book} on {self.borrow_date}"

    def clean(self):
        if self.expected_return_date < self.borrow_date:
            raise ValidationError(
                "Expected return date cannot be before borrow date.")
