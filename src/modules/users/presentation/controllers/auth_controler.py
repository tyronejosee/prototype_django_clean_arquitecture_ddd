from typing import ClassVar, cast

from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from src.modules.common.presentation.controllers.base_controller import BaseController
from src.modules.users.application.providers import get_create_user_use_case, get_logout_user_use_case
from src.modules.users.domain.exceptions import LogoutError, UserAlreadyExistsError, UserDomainError
from src.modules.users.presentation.schemas.auth_schemas import (
    login_schema,
    logout_schema,
    refresh_schema,
    register_schema,
    token_verify_schema,
)
from src.modules.users.presentation.serializers.auth_serializer import LogoutSerializer, RegisterSerializer
from src.modules.users.presentation.throttles import (
    LoginRateThrottle,
    LogoutRateThrottle,
    RefreshRateThrottle,
    RegisterRateThrottle,
    TokenVerifyRateThrottle,
)


@extend_schema_view(**register_schema)
class RegisterController(BaseController):
    permission_classes: ClassVar[list] = [AllowAny]
    throttle_map: dict = {"POST": RegisterRateThrottle}

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict, serializer.validated_data)
        use_case = get_create_user_use_case()

        try:
            user = use_case.execute(data)
            return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)
        except UserDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except UserAlreadyExistsError as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)


@extend_schema_view(**login_schema)
class LoginController(TokenObtainPairView, BaseController):
    """
    Obtains access and refresh JWT tokens.

    Extends `TokenObtainPairView` to provide custom OpenAPI schema
    support via drf-spectacular.
    """

    throttle_map: dict = {"POST": LoginRateThrottle}


@extend_schema_view(**refresh_schema)
class RefreshController(TokenRefreshView, BaseController):
    """
    Refreshes an access token using a valid refresh token.

    Extends `TokenRefreshView` to provide custom OpenAPI schema
    support via drf-spectacular.
    """

    throttle_map: dict = {"POST": RefreshRateThrottle}


@extend_schema_view(**token_verify_schema)
class TokenVerifyController(TokenVerifyView, BaseController):
    """
    Verifies the validity of a given JWT token.

    Extends `TokenVerifyView` to provide custom OpenAPI schema
    support via drf-spectacular.
    """

    throttle_map: dict = {"POST": TokenVerifyRateThrottle}


@extend_schema_view(**logout_schema)
class LogoutController(BaseController):
    permission_classes: ClassVar[list] = [AllowAny]
    serializer_class = None
    throttle_map: dict = {"POST": LogoutRateThrottle}

    def post(self, request: Request) -> Response:
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict, serializer.validated_data)
        use_case = get_logout_user_use_case()

        try:
            use_case.execute(data["refresh"])
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LogoutError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
