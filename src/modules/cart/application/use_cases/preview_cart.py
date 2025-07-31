from modules.cart.domain.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)


class PreviewCartUseCase:
    def __init__(self, repo: CartRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, data: dict) -> dict:
        return self.repo.preview(data)
