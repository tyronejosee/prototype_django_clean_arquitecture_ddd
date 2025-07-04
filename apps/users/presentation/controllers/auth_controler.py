from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.application.providers import get_create_user_use_case
from apps.users.domain.exceptions import UserAlreadyExistsError, UserDomainError
from apps.users.presentation.serializers import UserCreateSerializer, UserSerializer


class RegisterController(APIView):
    permission_classes: list = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            use_case = get_create_user_use_case()
            user = use_case.execute(serializer.validated_data)  # type: ignore[arg-type]
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
    permission_classes: list = [AllowAny]
    serializer_class = None

    def post(self, request, *args, **kwargs) -> Response:
        refresh_token = request.data.get("refresh")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
