from drf_spectacular.utils import OpenApiResponse, extend_schema

from src.modules.common.presentation.api_messages import API_MESSAGES
from src.modules.users.presentation.serializers.wishlist_serializer import (
    WishlistCreateSerializer,
    WishlistListSerializer,
)

wishlist_schema: dict = {
    "get": extend_schema(
        summary="List wishlist items for authenticated user",
        responses={
            200: OpenApiResponse(WishlistListSerializer(many=True), description=API_MESSAGES["OK"]),
        },
        tags=["users"],
    ),
    "post": extend_schema(
        summary="Add a product to the authenticated user's wishlist",
        request=WishlistCreateSerializer,
        responses={
            201: OpenApiResponse(WishlistListSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
        },
        auth=["jwt"],
        tags=["users"],
    ),
}

wishlist_detail_schema: dict = {
    "delete": extend_schema(
        summary="Remove a product from the authenticated user's wishlist",
        responses={
            204: OpenApiResponse(description=API_MESSAGES["OK"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
        },
        auth=["jwt"],
        tags=["users"],
    ),
}
