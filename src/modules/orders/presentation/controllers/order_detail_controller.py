from typing import ClassVar
from uuid import UUID

from modules.common.presentation.controllers.base_controller import BaseController
from modules.orders.application.providers import (
    get_cancel_order_use_case,
    get_get_order_use_case,
)
from modules.orders.domain.exceptions import OrderDomainError, OrderNotFoundError
from modules.orders.presentation.serializers.order_serializer import OrderSerializer
from modules.orders.presentation.throttles import (
    CancelOrderRateThrottle,
    RetrieveOrderRateThrottle,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class OrderDetailController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]
    throttle_map: dict = {
        "GET": RetrieveOrderRateThrottle,
        "DELETE": CancelOrderRateThrottle,
    }

    def get(self, request: Request, order_id: UUID) -> Response:
        use_case = get_get_order_use_case()
        try:
            order = use_case.execute(order_id=order_id)
            return Response(OrderSerializer(order).data)
        except OrderNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, order_id: UUID) -> Response:
        use_case = get_cancel_order_use_case()
        try:
            order = use_case.execute(order_id=order_id)
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        except OrderDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except OrderNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
