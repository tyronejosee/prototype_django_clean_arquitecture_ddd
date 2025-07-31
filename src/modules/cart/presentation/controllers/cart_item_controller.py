from typing import ClassVar
from uuid import UUID

from modules.cart.application.providers import (
    get_delete_cart_item_use_case,
    get_patch_cart_item_use_case,
)
from modules.cart.domain.exceptions import CartDomainError, CartItemNotFoundError
from modules.cart.domain.value_objects.item_quantity import ItemQuantity
from modules.cart.presentation.serializers.cart_serializer import (
    CartItemPatchSerializer,
    CartSerializer,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class CartItemController(APIView):
    permission_classes: ClassVar[list] = [IsAuthenticated]

    def patch(self, request: Request, item_id: UUID) -> Response:
        serializer = CartItemPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_patch_cart_item_use_case()
        try:
            data: dict = serializer.validated_data  # type: ignore[arg-type]
            cart = use_case.execute(
                user_id=request.user.id,
                item_id=item_id,
                quantity=ItemQuantity(data["quantity"]),
            )
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        except CartDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except CartItemNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, item_id: UUID) -> Response:
        use_case = get_delete_cart_item_use_case()
        try:
            cart = use_case.execute(user_id=request.user.id, item_id=item_id)
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        except CartDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except CartItemNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
