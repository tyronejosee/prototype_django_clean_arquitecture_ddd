from typing import ClassVar

from django.db import transaction
from modules.common.presentation.controllers.base_controller import BaseController
from modules.orders.domain.exceptions import OrderNotFoundError
from modules.payments.application.providers import get_initiate_payment_use_case
from modules.payments.domain.exceptions import PaymentDomainError
from modules.payments.presentation.serializers.initiate_payment_serializer import (
    InitiatePaymentSerializer,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class InitiatePaymentController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]

    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = InitiatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_initiate_payment_use_case()
        try:
            data = serializer.validated_data  # type: ignore[arg-type]
            result = use_case.execute(
                order_id=data["order_id"],  # type: ignore[arg-type]
                payment_method=data["payment_method"],  # type: ignore[arg-type]
                email=request.user.email,
            )
            return Response(result, status=status.HTTP_200_OK)
        except OrderNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PaymentDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
