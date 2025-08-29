from typing import ClassVar

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.common.presentation.controllers.base_controller import BaseController
from src.modules.payments.domain.exceptions import GatewayTimeoutError, GatewayTokenError, PaymentDomainError
from src.modules.payments.presentation.providers import get_capture_payment_use_case


class CapturePaymentController(BaseController):
    permission_classes: ClassVar[list] = [AllowAny]

    @transaction.atomic
    def post(self, request: Request, external_id: str) -> Response:
        use_case = get_capture_payment_use_case()

        try:
            result = use_case.execute(external_id=str(external_id))
            return Response(result, status=status.HTTP_200_OK)
        except PaymentDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except GatewayTokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except GatewayTimeoutError as e:
            return Response({"detail": str(e)}, status=status.HTTP_504_GATEWAY_TIMEOUT)
