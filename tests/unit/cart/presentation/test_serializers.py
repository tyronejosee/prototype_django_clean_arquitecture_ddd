from uuid import uuid4

from src.modules.cart.presentation.serializers.cart_serializer import (
    CartItemPatchSerializer,
    CartItemSerializer,
    CartSerializer,
)


class TestCartItemSerializer:
    def test_cart_item_serializer_valid_data(self) -> None:
        data = {"product_id": uuid4(), "quantity": 2}
        serializer = CartItemSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_cart_item_serializer_missing_required(self) -> None:
        serializer = CartItemSerializer(data={})
        assert not serializer.is_valid()
        assert "product_id" in serializer.errors
        assert "quantity" in serializer.errors


class TestCartSerializer:
    def test_cart_serializer_valid_data(self) -> None:
        data = {
            "user_id": uuid4(),
            "items": [],
        }
        serializer = CartSerializer(data=data)
        assert serializer.is_valid(), serializer.errors


class TestCartItemPatchSerializer:
    def test_cart_item_patch_serializer_valid(self) -> None:
        serializer = CartItemPatchSerializer(data={"quantity": 3})
        assert serializer.is_valid()

    def test_cart_item_patch_serializer_invalid(self) -> None:
        serializer = CartItemPatchSerializer(data={"quantity": 0})
        assert not serializer.is_valid()
        assert "quantity" in serializer.errors
