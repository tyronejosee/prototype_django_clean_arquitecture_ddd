from typing import ClassVar

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.presentation.controllers.base_controller import BaseController
from apps.common.presentation.pagination import paginate_queryset
from apps.orders.application.providers import (
    get_create_order_use_case,
    get_list_orders_use_case,
)
from apps.orders.domain.exceptions import OrderDomainError
from apps.orders.presentation.serializers.order_serializer import OrderSerializer
from apps.orders.presentation.throttles import (
    CreateOrderRateThrottle,
    ListOrdersRateThrottle,
)


class OrderListCreateController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]
    throttle_map: dict = {
        "GET": ListOrdersRateThrottle,
        "POST": CreateOrderRateThrottle,
    }

    def get(self, request: Request) -> Response:
        use_case = get_list_orders_use_case()
        orders = use_case.execute(user_id=request.user.id)
        response = paginate_queryset(request, orders, OrderSerializer)
        response.status_code = status.HTTP_200_OK
        return response

    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_create_order_use_case()
        try:
            order = use_case.execute(user_id=request.user.id)
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        except OrderDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
