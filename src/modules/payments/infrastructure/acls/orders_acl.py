from typing import override
from uuid import UUID

from src.modules.orders.infrastructure.models.order_model import OrderModel
from src.modules.payments.domain.contracts.orders_dtos import OrderDTO, OrderItemDTO
from src.modules.payments.domain.contracts.orders_service_interface import OrdersServiceInterface


class OrdersACL(OrdersServiceInterface):
    @override
    def get_order_by_id(self, order_id: UUID) -> OrderDTO | None:
        try:
            order = OrderModel.objects.prefetch_related("items").get(id=order_id)
        except OrderModel.DoesNotExist:
            return None

        items = [
            OrderItemDTO(product_id=item.product_id, quantity=item.quantity, unit_price=item.unit_price)
            for item in order.items.all()
        ]

        return OrderDTO(id=order.id, status=order.status, final_price=order.final_price, items=items)

    @override
    def update_status(self, order_id: UUID, status: str) -> bool:
        try:
            order = OrderModel.objects.get(id=order_id)
            order.status = status
            order.save()
            return True
        except OrderModel.DoesNotExist:
            return False
