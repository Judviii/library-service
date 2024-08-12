from rest_framework import serializers
from borrowings_service.models import Borrowing
from borrowings_service.serializers import BorrowingDetailSerializer
from payments_service.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    money_to_pay = serializers.SerializerMethodField()

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

    def get_money_to_pay(self, obj):
        borrowing = Borrowing.objects.get(id=obj.borrowing_id)
        duration = borrowing.expected_return_date - borrowing.borrow_date
        rate_per_day = borrowing.book.price_per_day
        total_cost = duration.days * rate_per_day

        return round(total_cost, 2)


class PaymentDetailSerializer(PaymentSerializer):
    borrowing_id = BorrowingDetailSerializer(many=False, read_only=True)
