from uuid import UUID

from src.modules.cart.domain.entities.cart import Cart
from src.modules.cart.domain.interfaces.cart_repository_interface import CartRepositoryInterface


class CreateCartUseCase:
    def __init__(self, repo: CartRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID) -> Cart:
        return self.repo.create(user_id=user_id)
