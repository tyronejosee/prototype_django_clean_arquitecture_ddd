from typing import ClassVar

from modules.cart.application.providers import get_preview_cart_use_case
from modules.cart.domain.exceptions import CartDomainError
from modules.cart.presentation.serializers.cart_serializer import CartPreviewSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class CartPreviewController(APIView):
    permission_classes: ClassVar[list] = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = CartPreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_preview_cart_use_case()
        try:
            result = use_case.execute(
                data=serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(result, status=status.HTTP_200_OK)
        except CartDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
