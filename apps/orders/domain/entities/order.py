from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from apps.orders.domain.entities.order_item import OrderItem
from apps.orders.domain.exceptions import OrderDomainError
from apps.orders.domain.value_objects.order_status import OrderStatus


@dataclass(kw_only=True, slots=True)
class Order:
    id: UUID
    user_id: UUID
    items: list[OrderItem]
    status: OrderStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None

    # Messages
    CANNOT_CANCEL_ORDER_MESSAGE: str = "Cannot cancel a shipped or cancelled order."

    def total(self) -> Decimal:
        return sum((item.total_price for item in self.items), Decimal("0.00"))

    def cancel(self) -> None:
        if self.status not in [OrderStatus.PENDING, OrderStatus.PAID]:
            raise OrderDomainError(self.CANNOT_CANCEL_ORDER_MESSAGE)
        self.status = OrderStatus.CANCELLED
