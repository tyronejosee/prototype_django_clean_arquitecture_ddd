from datetime import UTC, datetime
from decimal import Decimal
from typing import cast
from uuid import uuid4

from src.modules.orders.presentation.serializers.order_serializer import (
    OrderItemOutputSerializer,
    OrderOutputSerializer,
)


class TestOrderItemOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Given: valid order item data
        data = {
            "id": uuid4(),
            "product_id": uuid4(),
            "quantity": 3,
            "unit_price": Decimal("19.99"),
            "total_price": Decimal("59.97"),
        }

        # When: serializing the output
        serializer = OrderItemOutputSerializer(instance=data)
        result = cast(dict, serializer.data)

        # Then: output should match input
        assert result["id"] == str(data["id"])
        assert result["product_id"] == str(data["product_id"])
        assert result["quantity"] == 3
        assert Decimal(result["unit_price"]) == Decimal("19.99")
        assert Decimal(result["total_price"]) == Decimal("59.97")


class TestOrderOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Simulate a class that looks like an enum
        class FakeStatus:
            def __init__(self, value: str) -> None:
                self.value = value

        class FakeOrder:
            def __init__(self, **kwargs) -> None:
                self.__dict__.update(kwargs)

        # Given: valid order items
        order_item1 = {
            "id": uuid4(),
            "product_id": uuid4(),
            "quantity": 2,
            "unit_price": Decimal("10.00"),
            "total_price": Decimal("20.00"),
        }
        order_item2 = {
            "id": uuid4(),
            "product_id": uuid4(),
            "quantity": 1,
            "unit_price": Decimal("15.50"),
            "total_price": Decimal("15.50"),
        }

        # Given: valid order data como objeto
        order_instance = FakeOrder(
            id=uuid4(),
            user_id=uuid4(),
            status=FakeStatus("COMPLETED"),
            items=[order_item1, order_item2],
            created_at=datetime(2025, 9, 2, 12, 0, 0, tzinfo=UTC),
            updated_at=datetime(2025, 9, 2, 12, 30, 0, tzinfo=UTC),
            total=Decimal("35.50"),
            final_price=Decimal("30.50"),
            applied_discounts=["SUMMER2025"],
            coupon={"code": "SUMMER2025", "discount_percent": Decimal("5.00")},
            promotions=["Holiday Sale"],
        )

        # When: serializing the output
        serializer = OrderOutputSerializer(instance=order_instance)
        result = cast(dict, serializer.data)

        # Then: output should match input
        assert result["id"] == str(order_instance.id)  # type: ignore
        assert result["user_id"] == str(order_instance.user_id)  # type: ignore
        assert result["status"] == "COMPLETED"
        assert len(result["items"]) == 2
        assert result["items"][0]["id"] == str(order_item1["id"])
        assert Decimal(result["items"][0]["unit_price"]) == Decimal("10.00")
        assert Decimal(result["items"][1]["total_price"]) == Decimal("15.50")
        assert result["created_at"] == order_instance.created_at.isoformat().replace("+00:00", "Z")  # type: ignore
        assert result["updated_at"] == order_instance.updated_at.isoformat().replace("+00:00", "Z")  # type: ignore
        assert Decimal(result["total"]) == Decimal("35.50")
        assert Decimal(result["final_price"]) == Decimal("30.50")
        assert result["applied_discounts"] == ["SUMMER2025"]
        assert result["coupon"]["code"] == "SUMMER2025"
        assert result["promotions"] == ["Holiday Sale"]
