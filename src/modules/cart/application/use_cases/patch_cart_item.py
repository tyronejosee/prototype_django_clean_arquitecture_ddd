from uuid import UUID

from modules.cart.domain.entities.cart import Cart
from modules.cart.domain.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)
from modules.cart.domain.value_objects.item_quantity import ItemQuantity


class PatchCartItemUseCase:
    def __init__(self, repo: CartRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID, item_id: UUID, quantity: ItemQuantity) -> Cart:
        return self.repo.patch_item(
            user_id=user_id,
            item_id=item_id,
            quantity=quantity.value,
        )
