from uuid import UUID

from apps.orders.domain.entities.order import Order
from apps.orders.domain.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)


class GetOrderUseCase:
    def __init__(self, repo: OrderRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, order_id: UUID) -> Order:
        return self.repo.get_by_id(order_id)
