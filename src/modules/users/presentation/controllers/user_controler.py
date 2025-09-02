from typing import ClassVar, cast
from uuid import UUID

from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.common.presentation.controllers.base_controller import BaseController
from src.modules.users.application.providers import (
    get_create_user_use_case,
    get_deactivate_user_use_case,
    get_list_users_use_case,
    get_update_user_use_case,
    get_user_use_case,
)
from src.modules.users.domain.exceptions import UserAlreadyExistsError, UserDomainError, UserNotFoundError
from src.modules.users.presentation.schemas.user_schema import USER_DETAIL_SCHEMA, USER_LIST_CREATE_SCHEMA
from src.modules.users.presentation.serializers.user_serializer import UserCreateSerializer, UserSerializer
from src.modules.users.presentation.throttles import (
    CreateUserRateThrottle,
    DeleteUserRateThrottle,
    GetUserRateThrottle,
    ListUsersRateThrottle,
    UpdateUserRateThrottle,
)


@extend_schema_view(**USER_LIST_CREATE_SCHEMA)
class UserListCreateController(BaseController):
    permission_classes: ClassVar[list] = [IsAdminUser]
    throttle_map: dict = {"GET": ListUsersRateThrottle, "POST": CreateUserRateThrottle}

    def get(self, request: Request) -> Response:
        use_case = get_list_users_use_case()
        users = use_case.execute()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast("dict", serializer.validated_data)
        use_case = get_create_user_use_case()

        try:
            user = use_case.execute(data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except UserDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except UserAlreadyExistsError as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)


@extend_schema_view(**USER_DETAIL_SCHEMA)
class UserDetailController(BaseController):
    permission_classes: ClassVar[list] = [IsAdminUser]
    throttle_map: dict = {
        "GET": GetUserRateThrottle,
        "PUT": UpdateUserRateThrottle,
        "DELETE": DeleteUserRateThrottle,
    }

    def get(self, request: Request, user_id: UUID) -> Response:
        use_case = get_user_use_case()
        user = use_case.execute(user_id)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request: Request, user_id: UUID) -> Response:
        serializer = UserCreateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = cast("dict", serializer.validated_data)
        use_case = get_update_user_use_case()

        try:
            user = use_case.execute(user_id, data)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except UserNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except UserAlreadyExistsError as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

    def delete(self, request: Request, user_id: UUID) -> Response:
        use_case = get_deactivate_user_use_case()

        try:
            use_case.execute(user_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
