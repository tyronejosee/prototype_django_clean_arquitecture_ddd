from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers

from src.modules.catalog.presentation.serializers.category_serializer import (
    CategoryInputSerializer,
    CategoryOutputSerializer,
)
from src.modules.catalog.presentation.serializers.product_serializer import ProductOutputSerializer
from src.modules.common.presentation.api_messages import API_MESSAGES

category_list_create_schema: dict = {
    "get": extend_schema(
        summary="List all categories",
        responses={
            200: OpenApiResponse(
                inline_serializer(
                    name="PaginatedCategoryList",
                    fields={
                        "count": serializers.IntegerField(),
                        "next": serializers.CharField(allow_null=True),
                        "previous": serializers.CharField(allow_null=True),
                        "results": CategoryOutputSerializer(many=True),
                    },
                ),
                description=API_MESSAGES["OK"],
            ),
        },
        auth=[],
        tags=["catalog"],
    ),
    "post": extend_schema(
        summary="Create a new category",
        request=CategoryInputSerializer,
        responses={
            201: OpenApiResponse(CategoryOutputSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
        },
        tags=["catalog"],
    ),
}

category_detail_schema: dict = {
    "put": extend_schema(
        summary="Update a category by ID",
        request=CategoryInputSerializer,
        responses={
            200: OpenApiResponse(CategoryOutputSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
        },
        tags=["catalog"],
    ),
    "delete": extend_schema(
        summary="Deactivate a category by ID",
        responses={
            204: OpenApiResponse(description=API_MESSAGES["OK"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
        },
        tags=["catalog"],
    ),
}

category_product_list_schema: dict = {
    "get": extend_schema(
        summary="List all products by category",
        responses={
            200: OpenApiResponse(
                inline_serializer(
                    name="PaginatedCategoryProductList",
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
