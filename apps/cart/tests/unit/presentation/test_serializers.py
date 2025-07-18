from uuid import uuid4

from apps.cart.presentation.serializers.cart_serializer import (
    CartItemPatchSerializer,
    CartItemSerializer,
    CartPreviewSerializer,
    CartSerializer,
)


def test_cart_item_serializer_valid_data() -> None:
    data = {
        "product_id": uuid4(),
        "quantity": 2,
    }
    serializer = CartItemSerializer(data=data)
    assert serializer.is_valid(), serializer.errors


def test_cart_item_serializer_missing_required() -> None:
    serializer = CartItemSerializer(data={})
    assert not serializer.is_valid()
    assert "product_id" in serializer.errors
    assert "quantity" in serializer.errors


def test_cart_serializer_valid_data() -> None:
    data = {
        "user_id": uuid4(),
        "items": [
            {
                "product_id": uuid4(),
                "quantity": 1,
            }
        ],
    }
    serializer = CartSerializer(data=data)
    assert serializer.is_valid(), serializer.errors


def test_cart_serializer_missing_items() -> None:
    data = {
        "user_id": uuid4(),
    }
    serializer = CartSerializer(data=data)
    assert not serializer.is_valid()
    assert "items" in serializer.errors


def test_cart_item_patch_serializer_valid() -> None:
    serializer = CartItemPatchSerializer(data={"quantity": 3})
    assert serializer.is_valid()


def test_cart_item_patch_serializer_invalid() -> None:
    serializer = CartItemPatchSerializer(data={"quantity": 0})
    assert not serializer.is_valid()
    assert "quantity" in serializer.errors


def test_cart_preview_serializer_valid() -> None:
    data = {
        "user_id": uuid4(),
        "items": [{"product_id": uuid4(), "quantity": 2}],
    }
    serializer = CartPreviewSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
