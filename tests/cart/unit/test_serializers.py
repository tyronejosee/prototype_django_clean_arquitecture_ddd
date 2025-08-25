from datetime import UTC, datetime
from decimal import Decimal
from typing import cast
from uuid import uuid4

from src.modules.cart.presentation.serializers.cart_serializer import (
    QuantityInputSerializer,
    CartItemInputSerializer,
    CartItemOutputSerializer,
    CartInputSerializer,
    CartOutputSerializer,
)


class TestQuantityInputSerializer:
    def test_valid_data_returns_expected_fields(self) -> None:
        # Given: valid quantity input
        data = {"quantity": 2}

        # When: serializing the input
        serializer = QuantityInputSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)

        # Then: quantity should match
        assert result["quantity"] == 2

    def test_invalid_data_returns_error(self) -> None:
        # Given: invalid quantity (zero)
        data = {"quantity": 0}

        # When: validating input
        serializer = QuantityInputSerializer(data=data)

        # Then: should be invalid with "quantity" error
        assert not serializer.is_valid()
        assert "quantity" in serializer.errors


class TestCartItemInputSerializer:
    def test_valid_data_returns_expected_fields(self) -> None:
        # Given: valid cart item input
        data = {"product_id": uuid4(), "quantity": 3}

        # When: serializing the input
        serializer = CartItemInputSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)

        # Then: output should match input
        assert result["product_id"] == data["product_id"]
        assert result["quantity"] == 3

    def test_missing_fields_returns_errors(self) -> None:
        # Given: empty input
        data = {}

        # When: validating
        serializer = CartItemInputSerializer(data=data)

        # Then: both fields should raise errors
        assert not serializer.is_valid()
        assert "product_id" in serializer.errors
        assert "quantity" in serializer.errors

    def test_invalid_quantity_returns_error(self) -> None:
        # Given: invalid quantity
        data = {"product_id": uuid4(), "quantity": 0}

        # When: validating
        serializer = CartItemInputSerializer(data=data)

        # Then: should have error on quantity
        assert not serializer.is_valid()
        assert "quantity" in serializer.errors


class TestCartItemOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Given: valid cart item output data
        data = {
            "id": uuid4(),
            "product_id": uuid4(),
            "quantity": 5,
        }

        # When: serializing the output
        serializer = CartItemOutputSerializer(instance=data)
        result = cast(dict, serializer.data)

        # Then: output should match input
        assert result["id"] == str(data["id"])
        assert result["product_id"] == str(data["product_id"])
        assert result["quantity"] == 5


class TestCartInputSerializer:
    def test_valid_data_returns_expected_fields(self) -> None:
        # Given: cart with multiple items
        data = {
            "items": [
                {"product_id": uuid4(), "quantity": 2},
                {"product_id": uuid4(), "quantity": 1},
            ]
        }

        # When: validating
        serializer = CartInputSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)

        # Then: items should be preserved
        assert len(result["items"]) == 2
        assert result["items"][0]["quantity"] == 2

    def test_empty_items_list_is_valid(self) -> None:
        # Given: empty cart
        data = {"items": []}

        # When: validating
        serializer = CartInputSerializer(data=data)

        # Then: empty items should be valid
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)
        assert result["items"] == []


class TestCartOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Given: valid cart output data
        data = {
            "id": uuid4(),
            "user_id": uuid4(),
            "items": [
                {
                    "id": uuid4(),
                    "product_id": uuid4(),
                    "quantity": 2,
                }
            ],
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
            "total": Decimal("49.99"),
        }

        # When: serializing the output
        serializer = CartOutputSerializer(instance=data)
        result = cast(dict, serializer.data)

        # Then: all fields should match
        assert result["id"] == str(data["id"])
        assert result["user_id"] == str(data["user_id"])
        assert isinstance(result["items"], list)
        assert result["items"][0]["quantity"] == 2
        assert result["total"] == "49.99"
        assert result["created_at"] == data["created_at"].isoformat().replace("+00:00", "Z")
        assert result["updated_at"] == data["updated_at"].isoformat().replace("+00:00", "Z")
