from drf_spectacular.utils import OpenApiResponse, extend_schema

from src.modules.common.presentation.api_messages import API_MESSAGES
from src.modules.payments.presentation.serializers.payment_serializer import (
    CapturePaymentOutputSerializer,
    InitiatePaymentOutputSerializer,
)

INITIATE_PAYMENT_SCHEMA: dict = {
    "post": extend_schema(
        operation_id="initiate_payment",
        summary="Initialize payment based on the registered user's cart",
        request=None,
        responses={
            200: OpenApiResponse(InitiatePaymentOutputSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            502: OpenApiResponse(description=API_MESSAGES["BAD_GATEWAY"]),
            504: OpenApiResponse(description=API_MESSAGES["GATEWAY_TIMEOUT"]),
        },
        tags=["payments"],
    ),
}


CAPTURE_PAYMENT_SCHEMA: dict = {
    "post": extend_schema(
        operation_id="capture_payment",
        summary="Capture a payment (PayPal Only)",
        request=None,
        responses={
            200: OpenApiResponse(CapturePaymentOutputSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            502: OpenApiResponse(description=API_MESSAGES["BAD_GATEWAY"]),
            504: OpenApiResponse(description=API_MESSAGES["GATEWAY_TIMEOUT"]),
        },
        tags=["payments"],
    ),
}
