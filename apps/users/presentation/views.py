from uuid import UUID

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..application.providers import (
    get_authenticate_user_use_case,
    get_create_user_use_case,
    get_deactivate_user_use_case,
    get_list_users_use_case,
    get_update_user_use_case,
    get_user_use_case,
)
from ..domain.exceptions import (
    UserAlreadyExistsException,
    UserDomainException,
    UserNotFoundException,
)
from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserSerializer,
)


class UserListCreateView(APIView):
    permission_classes = [AllowAny]  # ! TODO: Add roles

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
            user = use_case.execute(
                user_data=serializer.validated_data,  # type: ignore[arg-type]
            )
            response_serializer = UserSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except UserDomainException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except UserAlreadyExistsException as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id: UUID) -> Response:
        use_case = get_user_use_case()
        user = use_case.execute(user_id=user_id)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id: UUID) -> Response:
        serializer = UserCreateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            use_case = get_update_user_use_case()
            user = use_case.execute(
                user_id=user_id,
                user_data=serializer.validated_data,  # type: ignore[arg-type]
            )
            response_serializer = UserSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except UserNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except UserAlreadyExistsException as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

    def delete(self, request, user_id: UUID) -> Response:
        try:
            use_case = get_deactivate_user_use_case()
            use_case.execute(user_id=user_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(APIView):
    permission_classes = [AllowAny]  # ! TODO: Add roles

    def post(self, request) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        use_case = get_authenticate_user_use_case()
        user = use_case.execute(email=email, password=password)

        if user:
            # ! TODO: Add token generation
            return Response(
                {"message": "Login successful", "user_id": str(user.id)},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
