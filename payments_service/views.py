import stripe

from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from payments_service.models import Payment
from payments_service.serializers import (
    PaymentSerializer, PaymentDetailSerializer
)

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing_id__user=user)

    @action(
        methods=["GET"],
        detail=True,
        url_path="create-checkout-session",
        permission_classes=[IsAuthenticated],
    )
    def create_checkout_session(self, request, pk=None):
        """Endpoint for getting session_id and session_url"""
        domain_url = "http://localhost:8000/api/payments/"
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url,
            cancel_url=domain_url,
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Payment for BOOK",
                        },
                        "unit_amount": 20000,
                    },
                    "quantity": 1,
                }
            ]
        )
        return JsonResponse(
            {
                "sessionId": checkout_session["id"],
                "sessionUrl": checkout_session["url"]
            }
        )
