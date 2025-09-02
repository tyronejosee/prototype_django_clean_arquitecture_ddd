from typing import ClassVar, cast
from uuid import UUID

from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.cart.domain.exceptions import CartDomainError, CartItemNotFoundError, CartNotFoundError
from src.modules.cart.domain.value_objects.item_quantity import ItemQuantity
from src.modules.cart.presentation.providers import (
    get_add_cart_items_use_case,
    get_create_cart_use_case,
    get_delete_cart_item_use_case,
    get_get_cart_use_case,
    get_patch_cart_item_use_case,
)
from src.modules.cart.presentation.schemas.cart_schema import (
    CART_ITEM_CREATE_SCHEMA,
    CART_ITEM_DETAIL_SCHEMA,
    CART_SCHEMA,
)
from src.modules.cart.presentation.serializers.cart_serializer import (
    CartInputSerializer,
    CartOutputSerializer,
    QuantityInputSerializer,
)
from src.modules.cart.presentation.throttles import (
    AddCartItemsRateThrottle,
    CreateCartRateThrottle,
    DeleteCartItemRateThrottle,
    ListCartRateThrottle,
    UpdateCartItemRateThrottle,
)
from src.modules.common.presentation.controllers.base_controller import BaseController


@extend_schema_view(**CART_SCHEMA)
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


@extend_schema_view(**CART_ITEM_CREATE_SCHEMA)
class CartItemController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]
    throttle_map: dict = {"POST": AddCartItemsRateThrottle}

    def post(self, request: Request) -> Response:
        serializer = CartInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast("dict", serializer.validated_data)
        items_data = validated_data.get("items", [])
        use_case = get_add_cart_items_use_case()

        try:
            cart = use_case.execute(user_id=request.user.id, items_data=items_data)
            return Response(CartOutputSerializer(cart).data, status=status.HTTP_201_CREATED)
        except CartDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(**CART_ITEM_DETAIL_SCHEMA)
class CartItemDetailController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]
    throttle_map: dict = {"PATCH": UpdateCartItemRateThrottle, "DELETE": DeleteCartItemRateThrottle}

    def patch(self, request: Request, item_id: UUID) -> Response:
        serializer = QuantityInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast("dict", serializer.validated_data)
        use_case = get_patch_cart_item_use_case()

        try:
            cart = use_case.execute(
                user_id=request.user.id,
                item_id=item_id,
                quantity=ItemQuantity(validated_data["quantity"]),
            )
            return Response(CartOutputSerializer(cart).data, status=status.HTTP_200_OK)
        except CartDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except CartItemNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, item_id: UUID) -> Response:
        use_case = get_delete_cart_item_use_case()

        try:
            cart = use_case.execute(user_id=request.user.id, item_id=item_id)
            return Response(CartOutputSerializer(cart).data, status=status.HTTP_200_OK)
        except CartDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except CartItemNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
