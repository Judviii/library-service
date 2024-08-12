from rest_framework import serializers
from borrowings_service.serializers import BorrowingDetailSerializer
from payments_service.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing_id",
            "session_url",
            "session_id",
            "money_to_pay"
        )


class PaymentDetailSerializer(PaymentSerializer):
    borrowing_id = BorrowingDetailSerializer(many=False, read_only=True)
