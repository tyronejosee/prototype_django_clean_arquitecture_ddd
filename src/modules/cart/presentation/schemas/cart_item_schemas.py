from drf_spectacular.utils import OpenApiResponse, extend_schema

from src.modules.cart.presentation.serializers.cart_serializer import (
    CartInputSerializer,
    CartOutputSerializer,
    QuantityInputSerializer,
)
from src.modules.common.presentation.api_messages import API_MESSAGES

cart_item_create_schema: dict = {
    "post": extend_schema(
        summary="Add items to the authenticated user's cart",
        request=CartInputSerializer,
        responses={
            201: OpenApiResponse(CartOutputSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
        },
        tags=["cart"],
    )
}


cart_item_detail_schema: dict = {
    "patch": extend_schema(
        summary="Update quantity of a cart item by ID",
        request=QuantityInputSerializer,
        responses={
            200: OpenApiResponse(CartOutputSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
        },
        tags=["cart"],
    ),
    "delete": extend_schema(
        summary="Remove a cart item by ID",
        responses={
            201: OpenApiResponse(description=API_MESSAGES["NO_CONTENT"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
        },
        tags=["cart"],
    ),
}
