from rest_framework import viewsets, mixins
from borrowings_service.models import Borrowing
from borrowings_service.serializers import (
    BorrowingSerializer, BorrowingDetailSerializer
)


class BorrowingViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer
