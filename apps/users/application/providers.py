from functools import lru_cache

from .use_cases.create_user import CreateUserUseCase
from .use_cases.list_users import ListUsersUseCase
from .use_cases.get_user import GetUserUseCase
from .use_cases.update_user import UpdateUserUseCase
from .use_cases.deactivate_user import DeactivateUserUseCase
from .use_cases.authenticate_user import AuthenticateUserUseCase
from ..domain.services.password_service import PasswordService
from ..infrastructure.repositories import UserRepository


@lru_cache()
def get_password_service() -> PasswordService:
    return PasswordService()


@lru_cache()
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


def get_authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(
        repo=get_user_repository(),
        password_service=get_password_service(),
    )
