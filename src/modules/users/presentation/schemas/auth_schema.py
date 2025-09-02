from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenVerifySerializer

from src.modules.common.presentation.api_messages import API_MESSAGES
from src.modules.users.presentation.serializers.auth_serializer import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
)

REGISTER_SCHEMA: dict = {
    "post": extend_schema(
        operation_id="register_user",
        summary="Register a new user",
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(RegisterSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["users"],
    ),
}

LOGIN_SCHEMA: dict = {
    "post": extend_schema(
        operation_id="login_user",
        summary="Login a user",
        request=LoginSerializer,
        responses={
            201: OpenApiResponse(LoginSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["users"],
    ),
}

REFRESH_SCHEMA: dict = {
    "post": extend_schema(
        operation_id="refresh_token",
        summary="Refresh a token",
        request=TokenRefreshSerializer,
        responses={
            200: OpenApiResponse(TokenRefreshSerializer, description=API_MESSAGES["OK"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["users"],
    ),
}

TOKEN_VERIFY_SCHEMA: dict = {
    "post": extend_schema(
        operation_id="verify_token",
        summary="Verify a token",
        request=TokenVerifySerializer,
        responses={
            200: OpenApiResponse(description=API_MESSAGES["OK"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["users"],
    ),
}

CHANGE_PASSWORD_SCHEMA: dict = {
    "patch": extend_schema(
        operation_id="change_password",
        summary="Change user password",
        description="Change the authenticated user's password",
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
            404: OpenApiResponse(description=API_MESSAGES["NOT_FOUND"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["users"],
    ),
}

LOGOUT_SCHEMA: dict = {
    "post": extend_schema(
        operation_id="logout_user",
        summary="Logout a user",
        request=LoginSerializer,
        responses={
            201: OpenApiResponse(LoginSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            429: OpenApiResponse(description=API_MESSAGES["TOO_MANY_REQUESTS"]),
        },
        tags=["users"],
    ),
}
