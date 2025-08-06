from functools import lru_cache

from src.modules.cart.application.use_cases.add_cart_items import AddCartItemsUseCase
from src.modules.cart.application.use_cases.create_cart import CreateCartUseCase
from src.modules.cart.application.use_cases.delete_cart_item import DeleteCartItemUseCase
from src.modules.cart.application.use_cases.get_cart import GetCartUseCase
from src.modules.cart.application.use_cases.patch_cart_item import PatchCartItemUseCase
from src.modules.cart.infrastructure.cache.cart_cache_service import CartCacheService
from src.modules.cart.infrastructure.repositories.cart_repository import CartRepository


@lru_cache
def get_cart_repository() -> CartRepository:
    return CartRepository()


@lru_cache
def get_cart_cache() -> CartCacheService:
    return CartCacheService()


def get_get_cart_use_case() -> GetCartUseCase:
    return GetCartUseCase(repo=get_cart_repository(), cache=get_cart_cache())


def get_create_cart_use_case() -> CreateCartUseCase:
    return CreateCartUseCase(repo=get_cart_repository())


def get_add_cart_items_use_case() -> AddCartItemsUseCase:
    return AddCartItemsUseCase(repo=get_cart_repository(), cache=get_cart_cache())


def get_patch_cart_item_use_case() -> PatchCartItemUseCase:
    return PatchCartItemUseCase(repo=get_cart_repository(), cache=get_cart_cache())


def get_delete_cart_item_use_case() -> DeleteCartItemUseCase:
    return DeleteCartItemUseCase(repo=get_cart_repository(), cache=get_cart_cache())
