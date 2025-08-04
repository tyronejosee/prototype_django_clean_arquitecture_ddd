from typing import ClassVar

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.modules.cart.application.providers import get_create_cart_use_case, get_get_cart_use_case
from src.modules.cart.domain.exceptions import CartDomainError, CartNotFoundError
from src.modules.cart.presentation.serializers.cart_serializer import CartSerializer


class CartController(APIView):
    permission_classes: ClassVar[list] = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user_id = request.user.id
        if not user_id:
            return Response(
                {"error": "No user_id in request."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        use_case = get_get_cart_use_case()
        try:
            cart = use_case.execute(user_id=user_id)
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        except CartNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request: Request) -> Response:
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_create_cart_use_case()
        try:
            data: dict = serializer.validated_data  # type: ignore[arg-type]
            data["user_id"] = request.user.id
            cart = use_case.execute(data)
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
        except CartDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
