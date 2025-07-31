from functools import lru_cache

from src.modules.cart.application.use_cases.create_cart import CreateCartUseCase
from src.modules.cart.application.use_cases.delete_cart_item import (
    DeleteCartItemUseCase,
)
from src.modules.cart.application.use_cases.get_cart import GetCartUseCase
from src.modules.cart.application.use_cases.patch_cart_item import PatchCartItemUseCase
from src.modules.cart.application.use_cases.preview_cart import PreviewCartUseCase
from src.modules.cart.application.use_cases.update_cart import UpdateCartUseCase
from src.modules.cart.infrastructure.repositories.cart_repository import CartRepository


@lru_cache
def get_cart_repository() -> CartRepository:
    return CartRepository()


def get_get_cart_use_case() -> GetCartUseCase:
    return GetCartUseCase(repo=get_cart_repository())


def get_create_cart_use_case() -> CreateCartUseCase:
    return CreateCartUseCase(repo=get_cart_repository())


def get_update_cart_use_case() -> UpdateCartUseCase:
    return UpdateCartUseCase(repo=get_cart_repository())


def get_patch_cart_item_use_case() -> PatchCartItemUseCase:
    return PatchCartItemUseCase(repo=get_cart_repository())


def get_delete_cart_item_use_case() -> DeleteCartItemUseCase:
    return DeleteCartItemUseCase(repo=get_cart_repository())


def get_preview_cart_use_case() -> PreviewCartUseCase:
    return PreviewCartUseCase(repo=get_cart_repository())
