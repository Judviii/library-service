from rest_framework import viewsets, mixins
from borrowings_service.models import Borrowing
from borrowings_service.serializers import (
    BorrowingSerializer, BorrowingDetailSerializer
)
from borrowings_service.helpers.telegrambot import (
    send_message, get_message
)


class BorrowingViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        message = get_message(borrowing)
        send_message(message)
