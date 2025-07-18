from uuid import UUID

from apps.cart.domain.entities.cart import Cart
from apps.cart.domain.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)


class GetCartUseCase:
    def __init__(self, repo: CartRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID) -> Cart:
        return self.repo.get_by_user(user_id=user_id)
