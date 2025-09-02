from drf_spectacular.utils import OpenApiResponse, extend_schema

from src.modules.common.presentation.api_messages import API_MESSAGES
from src.modules.users.presentation.serializers.user_serializer import UserCreateSerializer, UserSerializer

USER_LIST_CREATE_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="list_users",
        summary="List all users",
        responses={
            200: OpenApiResponse(UserSerializer(many=True), description=API_MESSAGES["OK"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["users"],
    ),
    "post": extend_schema(
        operation_id="create_user",
        summary="Create a new user",
        request=UserCreateSerializer,
        responses={
            201: OpenApiResponse(UserSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["users"],
    ),
}

USER_DETAIL_SCHEMA: dict = {
    "get": extend_schema(
        operation_id="get_user_details",
        summary="Get user details by ID",
        responses={
            200: OpenApiResponse(UserSerializer, description=API_MESSAGES["OK"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["users"],
    ),
    "put": extend_schema(
        operation_id="update_user",
        summary="Update a user by ID",
        request=UserCreateSerializer,
        responses={
            200: OpenApiResponse(UserSerializer, description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["users"],
    ),
    "delete": extend_schema(
        operation_id="deactivate_user",
        summary="Deactivate a user by ID",
        responses={
            204: OpenApiResponse(description=API_MESSAGES["OK"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            403: OpenApiResponse(description=API_MESSAGES["FORBIDDEN"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["users"],
    ),
}
