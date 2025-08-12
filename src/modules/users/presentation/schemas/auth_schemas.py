from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenVerifySerializer

from src.modules.common.presentation.api_messages import API_MESSAGES
from src.modules.users.presentation.serializers.auth_serializer import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
)

register_schema: dict = {
    "post": extend_schema(
        summary="Register a new user",
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(RegisterSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            409: OpenApiResponse(description=API_MESSAGES["CONFLICT"]),
        },
        tags=["users"],
    ),
}

login_schema: dict = {
    "post": extend_schema(
        summary="Login a user",
        request=LoginSerializer,
        responses={
            201: OpenApiResponse(LoginSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
        },
        tags=["users"],
    ),
}

refresh_schema: dict = {
    "post": extend_schema(
        summary="Verify a token",
        request=TokenRefreshSerializer,
        responses={
            200: OpenApiResponse(TokenRefreshSerializer, description=API_MESSAGES["OK"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
        },
        tags=["users"],
    ),
}

token_verify_schema: dict = {
    "post": extend_schema(
        summary="Verify a token",
        request=TokenVerifySerializer,
        responses={
            200: OpenApiResponse(description=API_MESSAGES["OK"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
        },
        tags=["users"],
    ),
}

change_password_schema: dict = {
    "patch": extend_schema(
        summary="Change user password",
        description="Change the authenticated user's password",
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description=API_MESSAGES["OK"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
            401: OpenApiResponse(description=API_MESSAGES["UNAUTHORIZED"]),
        },
        tags=["users"],
    ),
}

logout_schema: dict = {
    "post": extend_schema(
        summary="Logout a user",
        request=LoginSerializer,
        responses={
            201: OpenApiResponse(LoginSerializer, description=API_MESSAGES["CREATED"]),
            400: OpenApiResponse(description=API_MESSAGES["BAD_REQUEST"]),
        },
        tags=["users"],
    ),
}
