from django.urls import path
from django.urls.resolvers import URLPattern

from src.modules.payments.presentation.controllers.payment_controller import (
    CapturePaymentController,
    InitiatePaymentController,
)

app_name = "payments"

urlpatterns: list[URLPattern] = [
    path("payments", InitiatePaymentController.as_view(), name="initiate-payment"),
    path("payments/<str:external_id>/capture", CapturePaymentController.as_view(), name="capture-payment"),
]
