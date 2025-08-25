from drf_spectacular.utils import OpenApiResponse, extend_schema

from src.modules.cart.presentation.serializers.cart_serializer import CartOutputSerializer
from src.modules.common.presentation.api_messages import API_MESSAGES

cart_schema: dict = {
    "get": extend_schema(
        summary="Retrieve the authenticated user's cart",
        responses={
            200: OpenApiResponse(CartOutputSerializer, description=API_MESSAGES["OK"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
        },
        tags=["cart"],
    ),
    "post": extend_schema(
        summary="Create a new cart for the authenticated user",
        request=None,
        responses={
            201: OpenApiResponse(CartOutputSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
        },
        tags=["cart"],
    ),
}
