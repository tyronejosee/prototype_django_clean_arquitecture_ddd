from drf_spectacular.utils import OpenApiResponse, extend_schema

from src.modules.cart.presentation.serializers.cart_serializer import (
    CartInputSerializer,
    CartOutputSerializer,
    QuantityInputSerializer,
)
from src.modules.common.presentation.api_messages import API_MESSAGES

CART_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="get_cart",
        summary="Retrieve the authenticated user's cart",
        responses={
            200: OpenApiResponse(CartOutputSerializer, description=API_MESSAGES["OK"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["cart"],
    ),
    "post": extend_schema(
        operation_id="create_cart",
        summary="Create a new cart for the authenticated user",
        request=None,
        responses={
            201: OpenApiResponse(CartOutputSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["cart"],
    ),
}

CART_ITEM_CREATE_SCHEMA: dict = {
    "post": extend_schema(
        operation_id="add_cart_items",
        summary="Add items to the authenticated user's cart",
        request=CartInputSerializer,
        responses={
            201: OpenApiResponse(CartOutputSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["cart"],
    )
}


CART_ITEM_DETAIL_SCHEMA: dict = {
    "patch": extend_schema(
        operation_id="update_cart_item",
        summary="Update quantity of a cart item by ID",
        request=QuantityInputSerializer,
        responses={
            200: OpenApiResponse(CartOutputSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["cart"],
    ),
    "delete": extend_schema(
        operation_id="delete_cart_item",
        summary="Remove a cart item by ID",
        responses={
            201: OpenApiResponse(description=API_MESSAGES["NO_CONTENT"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["cart"],
    ),
}
