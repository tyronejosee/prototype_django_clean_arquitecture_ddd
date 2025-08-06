from uuid import UUID

from src.modules.cart.domain.entities.cart import Cart
from src.modules.cart.domain.interfaces.cart_cache_interface import CartCacheInterface
from src.modules.cart.domain.interfaces.cart_repository_interface import CartRepositoryInterface
from src.modules.cart.domain.utils.cart_cache_keys import CartCacheKeys


class GetCartUseCase:
    def __init__(self, repo: CartRepositoryInterface, cache: CartCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, user_id: UUID) -> Cart:
        key = CartCacheKeys.cart_user_key(user_id)

        cached = self.cache.get(key)
        if cached is not None:
            return cached

        cart = self.repo.get_by_user(user_id=user_id)
        if cart is not None:
            self.cache.set(key, cart)

        return cart
