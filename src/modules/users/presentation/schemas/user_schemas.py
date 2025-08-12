from drf_spectacular.utils import OpenApiResponse, extend_schema

from src.modules.common.presentation.api_messages import API_MESSAGES
from src.modules.users.presentation.serializers.user_serializer import UserCreateSerializer, UserSerializer

user_list_create_schema: dict = {
    "get": extend_schema(
        summary="List all users",
        responses={
            200: OpenApiResponse(UserSerializer(many=True), description=API_MESSAGES["OK"]),
        },
        tags=["users"],
    ),
    "post": extend_schema(
        summary="Create a new user",
        request=UserCreateSerializer,
        responses={
            201: OpenApiResponse(UserSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
        },
        tags=["users"],
    ),
}

user_detail_schema: dict = {
    "get": extend_schema(
        summary="Get user details by ID",
        responses={
            200: OpenApiResponse(UserSerializer, description=API_MESSAGES["OK"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
        },
        tags=["users"],
    ),
    "put": extend_schema(
        summary="Update a user by ID",
        request=UserCreateSerializer,
        responses={
            200: OpenApiResponse(UserSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
        },
        tags=["users"],
    ),
    "delete": extend_schema(
        summary="Deactivate a user by ID",
        responses={
            204: OpenApiResponse(description=API_MESSAGES["OK"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
        },
        tags=["users"],
    ),
}
