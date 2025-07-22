from uuid import UUID

from apps.orders.domain.entities.order import Order
from apps.orders.domain.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)
from apps.orders.domain.value_objects.order_status import OrderStatus


class UpdateOrderStatusUseCase:
    def __init__(self, repo: OrderRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, order_id: UUID, new_status: OrderStatus) -> Order:
        order = self.repo.get_by_id(order_id)
        order.status = new_status
        return self.repo.update(order)
