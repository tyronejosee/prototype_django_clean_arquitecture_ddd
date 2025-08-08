from functools import lru_cache

from src.modules.users.application.use_cases.add_to_wishlist import AddToWishlistUseCase
from src.modules.users.application.use_cases.create_user import CreateUserUseCase
from src.modules.users.application.use_cases.deactivate_user import DeactivateUserUseCase
from src.modules.users.application.use_cases.get_user import GetUserUseCase
from src.modules.users.application.use_cases.list_users import ListUsersUseCase
from src.modules.users.application.use_cases.list_wishlist import ListWishlistUseCase
from src.modules.users.application.use_cases.logout_user import LogoutUserUseCase
from src.modules.users.application.use_cases.remove_from_wishlist import RemoveFromWishlistUseCase
from src.modules.users.application.use_cases.update_user import UpdateUserUseCase
from src.modules.users.infrastructure.repositories.user_repository import UserRepository
from src.modules.users.infrastructure.repositories.wishlist_repository import WishlistRepository
from src.modules.users.infrastructure.services.password_service import PasswordService
from src.modules.users.infrastructure.services.token_service import TokenService


@lru_cache
def get_password_service() -> PasswordService:
    return PasswordService()


@lru_cache
def get_jwt_token_service() -> TokenService:
    return TokenService()


@lru_cache
def get_user_repository() -> UserRepository:
    return UserRepository()


@lru_cache
def get_wishlist_repository() -> WishlistRepository:
    return WishlistRepository()


def get_list_users_use_case() -> ListUsersUseCase:
    return ListUsersUseCase(repo=get_user_repository())


def get_create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase(repo=get_user_repository(), password_service=get_password_service())


def get_user_use_case() -> GetUserUseCase:
    return GetUserUseCase(repo=get_user_repository())


def get_update_user_use_case() -> UpdateUserUseCase:
    return UpdateUserUseCase(repo=get_user_repository(), password_service=get_password_service())


def get_deactivate_user_use_case() -> DeactivateUserUseCase:
    return DeactivateUserUseCase(repo=get_user_repository())


def get_logout_user_use_case() -> LogoutUserUseCase:
    return LogoutUserUseCase(token_service=get_jwt_token_service())


def get_add_to_wishlist_use_case() -> AddToWishlistUseCase:
    return AddToWishlistUseCase(repo=get_wishlist_repository())


def get_remove_from_wishlist_use_case() -> RemoveFromWishlistUseCase:
    return RemoveFromWishlistUseCase(repo=get_wishlist_repository())


def get_list_wishlist_use_case() -> ListWishlistUseCase:
    return ListWishlistUseCase(repo=get_wishlist_repository())
