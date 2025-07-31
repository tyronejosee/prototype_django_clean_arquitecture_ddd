from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from modules.orders.domain.entities.order import Order
from modules.orders.domain.entities.order_item import OrderItem
from modules.orders.domain.value_objects.order_status import OrderStatus


class OrderFactory:
    @staticmethod
    def from_dict(data: dict) -> Order:
        order_id = data.get("id", uuid4())
        return Order(
            id=order_id,
            user_id=data["user_id"],
            status=data.get("status", OrderStatus.PENDING),
            items=[
                OrderItem(
                    id=item.get("id", uuid4()),
                    order_id=order_id,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    unit_price=item["unit_price"],
                )
                for item in data.get("items", [])
            ],
            created_at=data.get("created_at", datetime.now(UTC)),
            updated_at=data.get("updated_at", datetime.now(UTC)),
            final_price=data.get("final_price", Decimal("0.00")),
            applied_discounts=data.get("applied_discounts", []),
            coupon=data.get("coupon"),
            promotions=data.get("promotions", []),
        )

    @staticmethod
    def from_model(order_model) -> Order:
        return Order(
            id=order_model.id,
            user_id=order_model.user_id,
            status=OrderStatus(order_model.status),
            items=[
                OrderItem(
                    id=item.id,
                    order_id=order_model.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in order_model.items.all()
            ],
            created_at=order_model.created_at,
            updated_at=order_model.updated_at,
        )
