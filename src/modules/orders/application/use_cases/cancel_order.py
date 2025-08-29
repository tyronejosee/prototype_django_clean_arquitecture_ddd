from uuid import UUID

from src.modules.orders.domain.entities.order import Order
from src.modules.orders.domain.interfaces.order_repository_interface import OrderRepositoryInterface


class CancelOrderUseCase:
    def __init__(self, repo: OrderRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, order_id: UUID) -> Order:
        order = self.repo.get_by_id(order_id)
        order.cancel()
        return self.repo.cancel(order_id)
