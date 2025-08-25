from typing import ClassVar, cast
from uuid import UUID

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.cart.domain.exceptions import CartDomainError, CartItemNotFoundError
from src.modules.cart.domain.value_objects.item_quantity import ItemQuantity
from src.modules.cart.presentation.providers import get_delete_cart_item_use_case, get_patch_cart_item_use_case
from src.modules.cart.presentation.serializers.cart_serializer import CartOutputSerializer, QuantityInputSerializer
from src.modules.cart.presentation.throttles import DeleteCartItemRateThrottle, UpdateCartItemRateThrottle
from src.modules.common.presentation.controllers.base_controller import BaseController


class CartItemDetailController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]
    throttle_map: dict = {"PATCH": UpdateCartItemRateThrottle, "DELETE": DeleteCartItemRateThrottle}

    def patch(self, request: Request, item_id: UUID) -> Response:
        serializer = QuantityInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast(dict, serializer.validated_data)
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
