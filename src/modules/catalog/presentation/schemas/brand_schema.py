from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers

from src.modules.catalog.presentation.serializers.brand_serializer import BrandInputSerializer, BrandOutputSerializer
from src.modules.catalog.presentation.serializers.product_serializer import ProductOutputSerializer
from src.modules.common.presentation.api_messages import API_MESSAGES

BRAND_LIST_CREATE_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="list_brands",
        summary="List all brands",
        responses={
            200: OpenApiResponse(
                inline_serializer(
                    name="PaginatedBrandList",
                    fields={
                        "count": serializers.IntegerField(),
                        "next": serializers.CharField(allow_null=True),
                        "previous": serializers.CharField(allow_null=True),
                        "results": BrandOutputSerializer(many=True),
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
        operation_id="create_brand",
        summary="Create a new user",
        request=BrandInputSerializer,
        responses={
            201: OpenApiResponse(BrandOutputSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["catalog"],
    ),
}

BRAND_DETAIL_SCHEMA: dict = {
    "put": extend_schema(
        operation_id="update_brand",
        summary="Update a brand by ID",
        request=BrandInputSerializer,
        responses={
            200: OpenApiResponse(BrandOutputSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["catalog"],
    ),
    "delete": extend_schema(
        summary="Deactivate a brand by ID",
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

BRAND_PRODUCT_LIST_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="list_brand_products",
        summary="List all products by brand",
        responses={
            200: OpenApiResponse(
                inline_serializer(
                    name="PaginatedBrandProductList",
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
