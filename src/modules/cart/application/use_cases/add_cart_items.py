from uuid import UUID

from src.modules.cart.domain.entities.cart import Cart
from src.modules.cart.domain.factories.cart_item_factory import CartItemFactory
from src.modules.cart.domain.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)


class AddCartItemsUseCase:
    def __init__(self, repo: CartRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID, items_data: dict) -> Cart:
        items = [CartItemFactory.from_dict(item_data) for item_data in items_data]
        return self.repo.add_items(user_id=user_id, items=items)
