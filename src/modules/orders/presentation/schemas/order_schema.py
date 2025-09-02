from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers

from src.modules.common.presentation.api_messages import API_MESSAGES
from src.modules.orders.presentation.serializers.order_serializer import OrderOutputSerializer

ORDER_LIST_CREATE_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="list_orders",
        summary="List all orders for the current user",
        responses={
            200: OpenApiResponse(
                inline_serializer(
                    name="PaginatedOrderList",
                    fields={
                        "count": serializers.IntegerField(),
                        "next": serializers.CharField(allow_null=True),
                        "previous": serializers.CharField(allow_null=True),
                        "results": OrderOutputSerializer(many=True),
                    },
                ),
                description=API_MESSAGES["OK"],
            ),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["orders"],
    ),
    "post": extend_schema(
        operation_id="create_order",
        summary="Create a new order based on cart",
        responses={
            201: OpenApiResponse(OrderOutputSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["orders"],
    ),
}


ORDER_DETAIL_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="get_order_details",
        summary="Get order details by ID",
        responses={
            200: OpenApiResponse(OrderOutputSerializer, description=API_MESSAGES["OK"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["orders"],
    ),
    "delete": extend_schema(
        operation_id="cancel_order",
        summary="Cancel an order by ID",
        responses={
            200: OpenApiResponse(OrderOutputSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["orders"],
    ),
}
