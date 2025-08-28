from typing import ClassVar, cast

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.common.presentation.controllers.base_controller import BaseController
from src.modules.payments.domain.exceptions import GatewayTimeoutError, GatewayTokenError, PaymentDomainError
from src.modules.payments.presentation.providers import get_initiate_payment_use_case
from src.modules.payments.presentation.serializers.initiate_payment_serializer import InitiatePaymentInputSerializer


class InitiatePaymentController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]

    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = InitiatePaymentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast(dict, serializer.validated_data)
        use_case = get_initiate_payment_use_case()

        try:
            result = use_case.execute(
                order_id=validated_data["order_id"],
                payment_method=validated_data["payment_method"],
                email=request.user.email,
            )
            return Response(result, status=status.HTTP_200_OK)
        except PaymentDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except GatewayTokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except GatewayTimeoutError as e:
            return Response({"detail": str(e)}, status=status.HTTP_504_GATEWAY_TIMEOUT)
