from typing import ClassVar

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.modules.cart.application.providers import get_add_cart_items_use_case
from src.modules.cart.domain.exceptions import CartDomainError
from src.modules.cart.presentation.serializers.cart_serializer import CartItemCreateSerializer, CartSerializer


class CartItemController(APIView):
    permission_classes: ClassVar[list] = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_add_cart_items_use_case()
        try:
            data: dict = serializer.validated_data  # type: ignore[arg-type]
            items_data = data.get("items", [])
            cart = use_case.execute(user_id=request.user.id, items_data=items_data)
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
        except CartDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
