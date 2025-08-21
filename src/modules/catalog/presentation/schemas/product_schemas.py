from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers

from src.modules.catalog.presentation.serializers.product_serializer import (
    ProductInputSerializer,
    ProductOutputSerializer,
)
from src.modules.common.presentation.api_messages import API_MESSAGES

product_list_create_schema: dict = {
    "get": extend_schema(
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
        },
        auth=[],
        tags=["catalog"],
    ),
    "post": extend_schema(
        summary="Create a new user",
        request=ProductInputSerializer,
        responses={
            201: OpenApiResponse(ProductOutputSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
        },
        tags=["catalog"],
    ),
}

product_detail_schema: dict = {
    "get": extend_schema(
        summary="Get product details by ID",
        responses={
            200: OpenApiResponse(ProductOutputSerializer, description=API_MESSAGES["OK"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
        },
        auth=[],
        tags=["catalog"],
    ),
    "put": extend_schema(
        summary="Update a user by ID",
        request=ProductInputSerializer,
        responses={
            200: OpenApiResponse(ProductOutputSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
        },
        tags=["catalog"],
    ),
    "delete": extend_schema(
        summary="Deactivate a product by ID",
        responses={
            204: OpenApiResponse(description=API_MESSAGES["OK"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
        },
        tags=["catalog"],
    ),
}

featured_products_schema: dict = {
    "get": extend_schema(
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
        },
        auth=[],
        tags=["catalog"],
    )
}
