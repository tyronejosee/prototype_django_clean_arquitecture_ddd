from uuid import UUID

from apps.orders.domain.entities.order import Order
from apps.orders.domain.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)


class ListOrdersUseCase:
    def __init__(self, repo: OrderRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID) -> list[Order]:
        return self.repo.list_by_user(user_id)
