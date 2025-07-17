from apps.cart.domain.entities.cart import Cart
from apps.cart.domain.factories.cart_factory import CartFactory
from apps.cart.domain.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)


class CreateCartUseCase:
    def __init__(self, repo: CartRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, data: dict) -> Cart:
        cart = CartFactory.from_dict(data)
        return self.repo.create(cart)
