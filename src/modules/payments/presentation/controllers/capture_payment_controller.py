from typing import ClassVar

from django.db import transaction
from modules.common.presentation.controllers.base_controller import BaseController
from modules.payments.application.providers import get_capture_payment_use_case
from modules.payments.domain.exceptions import PaymentDomainError
from modules.payments.presentation.serializers.capture_payment_serializer import (
    CapturePaymentSerializer,
)
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response


class CapturePaymentController(BaseController):
    permission_classes: ClassVar[list] = [AllowAny]

    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = CapturePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_capture_payment_use_case()
        try:
            result = use_case.execute(
                payment_data=serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(result, status=status.HTTP_200_OK)
        except PaymentDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
