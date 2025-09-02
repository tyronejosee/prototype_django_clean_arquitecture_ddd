from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers

from src.modules.common.presentation.api_messages import API_MESSAGES
from src.modules.marketing.presentation.serializers.coupon_serializer import (
    CouponInputSerializer,
    CouponOutputSerializer,
)

COUPON_LIST_CREATE_SCHEMA: dict = {
    "get": extend_schema(
        summary="List all coupons",
        responses={
            200: OpenApiResponse(
                inline_serializer(
                    name="PaginatedCouponList",
                    fields={
                        "count": serializers.IntegerField(),
                        "next": serializers.CharField(allow_null=True),
                        "previous": serializers.CharField(allow_null=True),
                        "results": CouponOutputSerializer(many=True),
                    },
                ),
                description=API_MESSAGES["OK"],
            ),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["marketing"],
    ),
    "post": extend_schema(
        summary="Create a coupon",
        request=CouponInputSerializer,
        responses={
            201: OpenApiResponse(CouponOutputSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["marketing"],
    ),
}
