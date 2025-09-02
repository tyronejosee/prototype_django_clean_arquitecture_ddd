from typing import ClassVar
from uuid import UUID

from django.db import transaction
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.common.presentation.controllers.base_controller import BaseController
from src.modules.common.presentation.pagination import paginate_queryset
from src.modules.orders.domain.exceptions import OrderDomainError, OrderNotFoundError
from src.modules.orders.presentation.providers import (
    get_cancel_order_use_case,
    get_create_order_use_case,
    get_get_order_use_case,
    get_list_orders_use_case,
)
from src.modules.orders.presentation.schemas.order_schema import ORDER_DETAIL_SCHEMA, ORDER_LIST_CREATE_SCHEMA
from src.modules.orders.presentation.serializers.order_serializer import OrderOutputSerializer
from src.modules.orders.presentation.throttles import (
    CancelOrderRateThrottle,
    CreateOrderRateThrottle,
    ListOrdersRateThrottle,
    RetrieveOrderRateThrottle,
)


@extend_schema_view(**ORDER_LIST_CREATE_SCHEMA)
class OrderListCreateController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]
    serializer_class = OrderOutputSerializer
    throttle_map: dict = {"GET": ListOrdersRateThrottle, "POST": CreateOrderRateThrottle}

    def get(self, request: Request) -> Response:
        use_case = get_list_orders_use_case()
        orders = use_case.execute(user_id=request.user.id)
        response = paginate_queryset(request, orders, self.serializer_class)
        response.status_code = status.HTTP_200_OK
        return response

    @transaction.atomic
    def post(self, request: Request) -> Response:
        use_case = get_create_order_use_case()

        try:
            order = use_case.execute(user_id=request.user.id)
            return Response(self.serializer_class(order).data, status=status.HTTP_201_CREATED)
        except OrderDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(**ORDER_DETAIL_SCHEMA)
class OrderDetailController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]
    throttle_map: dict = {"GET": RetrieveOrderRateThrottle, "DELETE": CancelOrderRateThrottle}

    def get(self, request: Request, order_id: UUID) -> Response:
        use_case = get_get_order_use_case()

        try:
            order = use_case.execute(order_id=order_id)
            return Response(OrderOutputSerializer(order).data)
        except OrderNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, order_id: UUID) -> Response:
        use_case = get_cancel_order_use_case()

        try:
            order = use_case.execute(order_id=order_id)
            return Response(OrderOutputSerializer(order).data, status=status.HTTP_200_OK)
        except OrderDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except OrderNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
