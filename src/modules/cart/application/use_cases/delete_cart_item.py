from uuid import UUID

from modules.cart.domain.entities.cart import Cart
from modules.cart.domain.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)


class DeleteCartItemUseCase:
    def __init__(self, repo: CartRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID, item_id: UUID) -> Cart:
        return self.repo.delete_item(user_id=user_id, item_id=item_id)
