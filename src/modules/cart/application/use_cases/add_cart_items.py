from uuid import UUID

from src.modules.cart.domain.entities.cart import Cart
from src.modules.cart.domain.factories.cart_item_factory import CartItemFactory
from src.modules.cart.domain.interfaces.cart_cache_interface import CartCacheInterface
from src.modules.cart.domain.interfaces.cart_repository_interface import CartRepositoryInterface
from src.modules.cart.domain.utils.cart_cache_keys import CartCacheKeys


class AddCartItemsUseCase:
    def __init__(self, repo: CartRepositoryInterface, cache: CartCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, user_id: UUID, items_data: dict) -> Cart:
        items = [CartItemFactory.from_dict(item_data) for item_data in items_data]
        cart = self.repo.add_items(user_id=user_id, items=items)
        self.cache.delete(CartCacheKeys.cart_user_key(user_id))
        return cart
