from typing import ClassVar, cast

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from src.modules.users.application.providers import get_create_user_use_case, get_logout_user_use_case
from src.modules.users.domain.exceptions import LogoutError, UserAlreadyExistsError, UserDomainError
from src.modules.users.presentation.serializers.user_serializer import (
    UserCreateSerializer,
    UserLogoutSerializer,
    UserSerializer,
)


class RegisterController(APIView):
    permission_classes: ClassVar[list] = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict, serializer.validated_data)
        use_case = get_create_user_use_case()

        try:
            user = use_case.execute(data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except UserDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except UserAlreadyExistsError as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)


class LoginController(TokenObtainPairView):
    """
    Obtains access and refresh JWT tokens.

    Extends `TokenObtainPairView` to provide custom OpenAPI schema
    support via drf-spectacular.
    """


class RefreshController(TokenRefreshView):
    """
    Refreshes an access token using a valid refresh token.

    Extends `TokenRefreshView` to provide custom OpenAPI schema
    support via drf-spectacular.
    """


class TokenVerifyController(TokenVerifyView):
    """
    Verifies the validity of a given JWT token.

    Extends `TokenVerifyView` to provide custom OpenAPI schema
    support via drf-spectacular.
    """


class LogoutController(APIView):
    permission_classes: ClassVar[list] = [AllowAny]
    serializer_class = None

    def post(self, request, *args, **kwargs) -> Response:
        serializer = UserLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict, serializer.validated_data)
        use_case = get_logout_user_use_case()

        try:
            use_case.execute(data["refresh"])
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LogoutError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
