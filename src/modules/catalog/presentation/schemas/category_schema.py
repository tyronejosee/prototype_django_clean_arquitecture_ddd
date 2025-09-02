from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers

from src.modules.catalog.presentation.serializers.category_serializer import (
    CategoryInputSerializer,
    CategoryOutputSerializer,
)
from src.modules.catalog.presentation.serializers.product_serializer import ProductOutputSerializer
from src.modules.common.presentation.api_messages import API_MESSAGES

CATEGORY_LIST_CREATE_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="list_categories",
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
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        auth=[],
        tags=["catalog"],
    ),
    "post": extend_schema(
        operation_id="create_category",
        summary="Create a new category",
        request=CategoryInputSerializer,
        responses={
            201: OpenApiResponse(CategoryOutputSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["catalog"],
    ),
}

CATEGORY_DETAIL_SCHEMA: dict = {
    "put": extend_schema(
        operation_id="update_category",
        summary="Update a category by ID",
        request=CategoryInputSerializer,
        responses={
            200: OpenApiResponse(CategoryOutputSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["catalog"],
    ),
    "delete": extend_schema(
        operation_id="delete_category",
        summary="Deactivate a category by ID",
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

CATEGORY_PRODUCT_LIST_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="list_category_products",
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
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        auth=[],
        tags=["catalog"],
    )
}
