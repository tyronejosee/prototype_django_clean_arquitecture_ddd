from typing import ClassVar, cast

from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.cart.domain.exceptions import CartDomainError
from src.modules.cart.presentation.providers import get_add_cart_items_use_case
from src.modules.cart.presentation.schemas.cart_item_schemas import cart_item_create_schema
from src.modules.cart.presentation.serializers.cart_serializer import CartInputSerializer, CartOutputSerializer
from src.modules.cart.presentation.throttles import AddCartItemsRateThrottle
from src.modules.common.presentation.controllers.base_controller import BaseController


@extend_schema_view(**cart_item_create_schema)
class CartItemController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]
    throttle_map: dict = {"POST": AddCartItemsRateThrottle}

    def post(self, request: Request) -> Response:
        serializer = CartInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast(dict, serializer.validated_data)
        items_data = validated_data.get("items", [])
        use_case = get_add_cart_items_use_case()

        try:
            cart = use_case.execute(user_id=request.user.id, items_data=items_data)
            return Response(CartOutputSerializer(cart).data, status=status.HTTP_201_CREATED)
        except CartDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
