from typing import ClassVar

from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.cart.domain.exceptions import CartDomainError, CartNotFoundError
from src.modules.cart.presentation.providers import get_create_cart_use_case, get_get_cart_use_case
from src.modules.cart.presentation.schemas.cart_schemas import cart_schema
from src.modules.cart.presentation.serializers.cart_serializer import CartOutputSerializer
from src.modules.cart.presentation.throttles import CreateCartRateThrottle, ListCartRateThrottle
from src.modules.common.presentation.controllers.base_controller import BaseController


@extend_schema_view(**cart_schema)
class CartController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]
    throttle_map: dict = {"GET": ListCartRateThrottle, "POST": CreateCartRateThrottle}

    def get(self, request: Request) -> Response:
        use_case = get_get_cart_use_case()

        try:
            cart = use_case.execute(user_id=request.user.id)
            return Response(CartOutputSerializer(cart).data, status=status.HTTP_200_OK)
        except CartNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request: Request) -> Response:
        use_case = get_create_cart_use_case()

        try:
            cart = use_case.execute(request.user.id)
            return Response(CartOutputSerializer(cart).data, status=status.HTTP_201_CREATED)
        except CartDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
