from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from books_service.models import Book
from books_service.serializers import BookSerializer, BookListSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return BookSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy", "update", "partial_update"]:
            permission_classes = [IsAdminUser, ]
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [AllowAny, ]

        return [permission() for permission in permission_classes]
