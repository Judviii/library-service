from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from books_service.models import Book
from books_service.serializers import BookListSerializer


class UnauthenticatedBooksServiceAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_list_not_required(self):
        res = self.client.get(reverse("books:book-list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_required(self):
        res = self.client.get(reverse("books:book-detail", kwargs={"pk": 1}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBooksServiceAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@case.test", password="test123password"
        )
        self.client.force_authenticate(self.user)

    def test_book_list(self):
        book = Book.objects.create(
            title="TEST",
            author="TEST",
            inventory=99,
            daily_fee="20.05"
        )

        res = self.client.get(reverse("books:book-list"))
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_delete_auth_required(self):
        res = self.client.delete(
            reverse("books:book-detail", kwargs={"pk": 1})
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBooksServiceApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@case.test",
            password="test123password",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "TEST",
            "author": "TEST",
            "inventory": 99,
            "daily_fee": "20.05"
        }

        res = self.client.post(
            reverse("books_service:book-list"), data=payload
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
