from django.urls import path
from django.urls.resolvers import URLPattern

from src.modules.payments.presentation.controllers.capture_payment_controller import (
    CapturePaymentController,
)
from src.modules.payments.presentation.controllers.initiate_payment_controller import (
    InitiatePaymentController,
)

app_name = "payments"

urlpatterns: list[URLPattern] = [
    path(
        "payments",
        InitiatePaymentController.as_view(),
        name="order-pay",
    ),
    path(
        "payments/complete",
        CapturePaymentController.as_view(),
        name="order-pay-complete",
    ),
]
