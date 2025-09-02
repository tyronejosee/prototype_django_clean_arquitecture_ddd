from datetime import UTC, datetime
from decimal import Decimal
from typing import cast
from uuid import uuid4

from src.modules.marketing.presentation.serializers.coupon_serializer import (
    CouponInputSerializer,
    CouponOutputSerializer,
)
from src.modules.marketing.presentation.serializers.promotion_serializer import (
    PromotionInputSerializer,
    PromotionOutputSerializer,
)


class TestCouponInputSerializer:
    def test_valid_data_returns_expected_fields(self) -> None:
        # Given: valid input coupon data
        data = {
            "code": "SUMMER2025",
            "discount_percent": "15.50",
            "is_active": True,
            "max_uses": 100,
            "expires_at": datetime(2025, 12, 31, 23, 59, 59, tzinfo=UTC),
        }

        # When: serializing the input
        serializer = CouponInputSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)

        # Then: output should match input
        assert result["code"] == "SUMMER2025"
        assert Decimal(result["discount_percent"]) == Decimal("15.50")
        assert result["is_active"] is True
        assert result["max_uses"] == 100
        assert result["expires_at"] == datetime(2025, 12, 31, 23, 59, 59, tzinfo=UTC)


class TestCouponOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Given: valid output coupon data
        data = {
            "id": uuid4(),
            "code": "WINTER2025",
            "discount_percent": Decimal("20.00"),
            "is_active": False,
            "max_uses": 50,
            "used_count": 10,
            "expires_at": datetime(2025, 6, 30, 23, 59, 59, tzinfo=UTC),
        }

        # When: serializing the output
        serializer = CouponOutputSerializer(instance=data)
        result = cast(dict, serializer.data)

        # Then: output should match input
        assert result["id"] == str(data["id"])
        assert result["code"] == "WINTER2025"
        assert Decimal(result["discount_percent"]) == Decimal("20.00")
        assert result["is_active"] is False
        assert result["max_uses"] == 50
        assert result["used_count"] == 10
        assert result["expires_at"] == data["expires_at"].isoformat().replace("+00:00", "Z")


class TestPromotionInputSerializer:
    def test_valid_data_returns_expected_fields(self) -> None:
        # Given: valid input promotion data
        data = {
            "name": "Holiday Sale",
            "description": "End of year discounts on all products",
            "discount_percent": "25.00",
            "is_active": True,
            "starts_at": datetime(2025, 12, 1, 0, 0, 0, tzinfo=UTC),
            "ends_at": datetime(2025, 12, 31, 23, 59, 59, tzinfo=UTC),
        }

        # When: serializing the input
        serializer = PromotionInputSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)

        # Then: output should match input
        assert result["name"] == "Holiday Sale"
        assert result["description"] == "End of year discounts on all products"
        assert Decimal(result["discount_percent"]) == Decimal("25.00")
        assert result["is_active"] is True
        assert result["starts_at"] == datetime(2025, 12, 1, 0, 0, 0, tzinfo=UTC)
        assert result["ends_at"] == datetime(2025, 12, 31, 23, 59, 59, tzinfo=UTC)


class TestPromotionOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Given: valid output promotion data
        data = {
            "id": uuid4(),
            "name": "Summer Sale",
            "description": "Hot deals for summer",
            "discount_percent": Decimal("15.50"),
            "is_active": False,
            "starts_at": datetime(2025, 6, 1, 0, 0, 0, tzinfo=UTC),
            "ends_at": datetime(2025, 6, 30, 23, 59, 59, tzinfo=UTC),
        }

        # When: serializing the output
        serializer = PromotionOutputSerializer(instance=data)
        result = cast(dict, serializer.data)

        # Then: output should match input
        assert result["id"] == str(data["id"])
        assert result["name"] == "Summer Sale"
        assert result["description"] == "Hot deals for summer"
        assert Decimal(result["discount_percent"]) == Decimal("15.50")
        assert result["is_active"] is False
        assert result["starts_at"] == data["starts_at"].isoformat().replace("+00:00", "Z")
        assert result["ends_at"] == data["ends_at"].isoformat().replace("+00:00", "Z")
