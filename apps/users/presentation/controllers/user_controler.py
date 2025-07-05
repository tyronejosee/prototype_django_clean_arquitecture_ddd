from typing import ClassVar
from uuid import UUID

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.application.providers import (
    get_create_user_use_case,
    get_deactivate_user_use_case,
    get_list_users_use_case,
    get_update_user_use_case,
    get_user_use_case,
)
from apps.users.domain.exceptions import (
    UserAlreadyExistsError,
    UserDomainError,
    UserNotFoundError,
)
from apps.users.presentation.serializers.user_serializer import (
    UserCreateSerializer,
    UserSerializer,
)


class UserListCreateController(APIView):
    permission_classes: ClassVar[list] = [AllowAny]  # TODO: Add admin role

    def get(self, request) -> Response:
        use_case = get_list_users_use_case()
        users = use_case.execute()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request) -> Response:
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


class UserDetailController(APIView):
    permission_classes: ClassVar[list] = [AllowAny]  # TODO: Add admin role

    def get(self, request, user_id: UUID) -> Response:
        use_case = get_user_use_case()
        user = use_case.execute(user_id)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request, user_id: UUID) -> Response:
        serializer = UserCreateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            use_case = get_update_user_use_case()
            user = use_case.execute(
                user_id,
                serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except UserNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except UserAlreadyExistsError as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

    def delete(self, request, user_id: UUID) -> Response:
        try:
            use_case = get_deactivate_user_use_case()
            use_case.execute(user_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
