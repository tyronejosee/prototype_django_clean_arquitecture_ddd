from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from modules.orders.domain.entities.order_item import OrderItem
from modules.orders.domain.exceptions import OrderDomainError
from modules.orders.domain.value_objects.order_status import OrderStatus


@dataclass(kw_only=True, slots=True)
class Order:
    id: UUID
    user_id: UUID
    items: list[OrderItem]
    status: OrderStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None

    final_price: Decimal = Decimal("0.00")
    applied_discounts: list[str] = field(default_factory=list)
    coupon: dict | None = None
    promotions: list[dict] = field(default_factory=list)

    # Messages
    CANNOT_CANCEL_ORDER_MESSAGE: str = "Cannot cancel a shipped or cancelled order."

    def total(self) -> Decimal:
        return sum((item.total_price for item in self.items), Decimal("0.00"))

    def cancel(self) -> None:
        if self.status not in [OrderStatus.PENDING, OrderStatus.PAID]:
            raise OrderDomainError(self.CANNOT_CANCEL_ORDER_MESSAGE)
        self.status = OrderStatus.CANCELLED
