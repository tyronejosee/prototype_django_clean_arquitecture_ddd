from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers

from src.modules.catalog.presentation.serializers.product_serializer import (
    ProductInputSerializer,
    ProductOutputSerializer,
)
from src.modules.common.presentation.api_messages import API_MESSAGES

PRODUCT_LIST_CREATE_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="list_products",
        summary="List all products",
        responses={
            200: OpenApiResponse(
                inline_serializer(
                    name="PaginatedProductList",
                    fields={
                        "count": serializers.IntegerField(),
                        "next": serializers.CharField(allow_null=True),
                        "previous": serializers.CharField(allow_null=True),
                        "results": ProductOutputSerializer(many=True),
                    },
                ),
                description=API_MESSAGES["OK"],
            ),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        auth=[],
        tags=["catalog"],
    ),
    "post": extend_schema(
        operation_id="create_product",
        summary="Create a new user",
        request=ProductInputSerializer,
        responses={
            201: OpenApiResponse(ProductOutputSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["catalog"],
    ),
}

PRODUCT_DETAIL_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="get_product_details",
        summary="Get product details by ID",
        responses={
            200: OpenApiResponse(ProductOutputSerializer, description=API_MESSAGES["OK"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        auth=[],
        tags=["catalog"],
    ),
    "put": extend_schema(
        operation_id="update_product",
        summary="Update a user by ID",
        request=ProductInputSerializer,
        responses={
            200: OpenApiResponse(ProductOutputSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["catalog"],
    ),
    "delete": extend_schema(
        operation_id="delete_product",
        summary="Deactivate a product by ID",
        responses={
            204: OpenApiResponse(description=API_MESSAGES["OK"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["catalog"],
    ),
}

FEATURED_PRODUCTS_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="list_featured_products",
        summary="List all featured products",
        responses={
            200: OpenApiResponse(
                inline_serializer(
                    name="PaginatedFeaturedProductList",
                    fields={
                        "count": serializers.IntegerField(),
                        "next": serializers.CharField(allow_null=True),
                        "previous": serializers.CharField(allow_null=True),
                        "results": ProductOutputSerializer(many=True),
                    },
                ),
                description=API_MESSAGES["OK"],
            ),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        auth=[],
        tags=["catalog"],
    )
}
