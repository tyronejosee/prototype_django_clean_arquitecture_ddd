from functools import lru_cache

from apps.users.application.use_cases.logout_user import LogoutUserUseCase
from apps.users.infrastructure.repositories.user_repository import UserRepository
from apps.users.infrastructure.services.password_service import PasswordService
from apps.users.infrastructure.services.token_service import TokenService

from .use_cases.create_user import CreateUserUseCase
from .use_cases.deactivate_user import DeactivateUserUseCase
from .use_cases.get_user import GetUserUseCase
from .use_cases.list_users import ListUsersUseCase
from .use_cases.update_user import UpdateUserUseCase


@lru_cache
def get_password_service() -> PasswordService:
    return PasswordService()


@lru_cache
def get_jwt_token_service() -> TokenService:
    return TokenService()


@lru_cache
def get_user_repository() -> UserRepository:
    return UserRepository()


def get_list_users_use_case() -> ListUsersUseCase:
    return ListUsersUseCase(
        repo=get_user_repository(),
    )


def get_create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase(
        repo=get_user_repository(),
        password_service=get_password_service(),
    )


def get_user_use_case() -> GetUserUseCase:
    return GetUserUseCase(
        repo=get_user_repository(),
    )


def get_update_user_use_case() -> UpdateUserUseCase:
    return UpdateUserUseCase(
        repo=get_user_repository(),
        password_service=get_password_service(),
    )


def get_deactivate_user_use_case() -> DeactivateUserUseCase:
    return DeactivateUserUseCase(
        repo=get_user_repository(),
    )


def get_logout_user_use_case() -> LogoutUserUseCase:
    return LogoutUserUseCase(
        token_service=get_jwt_token_service(),
    )
