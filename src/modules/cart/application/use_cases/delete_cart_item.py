from uuid import UUID

from src.modules.cart.domain.interfaces.cart_cache_interface import CartCacheInterface
from src.modules.cart.domain.interfaces.cart_repository_interface import CartRepositoryInterface
from src.modules.cart.domain.utils.cart_cache_keys import CartCacheKeys


class DeleteCartItemUseCase:
    def __init__(self, repo: CartRepositoryInterface, cache: CartCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, user_id: UUID, item_id: UUID) -> None:
        self.repo.delete_item(user_id=user_id, item_id=item_id)
        self.cache.delete(CartCacheKeys.cart_user_key(user_id))
