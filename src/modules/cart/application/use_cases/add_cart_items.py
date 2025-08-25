from uuid import UUID

from src.modules.cart.domain.contracts.product_catalog_interface import ProductCatalogInterface
from src.modules.cart.domain.entities.cart import Cart
from src.modules.cart.domain.exceptions import CartDomainError
from src.modules.cart.domain.factories.cart_item_factory import CartItemFactory
from src.modules.cart.domain.interfaces.cart_cache_interface import CartCacheInterface
from src.modules.cart.domain.interfaces.cart_repository_interface import CartRepositoryInterface
from src.modules.cart.domain.utils.cart_cache_keys import CartCacheKeys


class AddCartItemsUseCase:
    # Messages
    PRODUCT_NOT_FOUND_MSG: str = "Product {product_id} does not exist."

    def __init__(
        self,
        repo: CartRepositoryInterface,
        cache: CartCacheInterface,
        product_catalog: ProductCatalogInterface,
    ) -> None:
        self.repo = repo
        self.cache = cache
        self.product_catalog = product_catalog

    def execute(self, user_id: UUID, items_data: dict) -> Cart:
        items = []

        for item_data in items_data:
            product_id = item_data["product_id"]
            if not self.product_catalog.exists(product_id):
                raise CartDomainError(self.PRODUCT_NOT_FOUND_MSG.format(product_id=product_id))

            items.append(CartItemFactory.from_dict(item_data))

        cart = self.repo.add_items(user_id=user_id, items=items)
        self.cache.delete(CartCacheKeys.cart_user_key(user_id))
        return cart
