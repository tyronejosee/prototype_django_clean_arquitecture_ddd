import pytest
from decimal import Decimal
from uuid import uuid4

from modules.cart.domain.entities.cart import Cart
from modules.cart.domain.exceptions import (
    CartDomainError,
    CartItemNotFoundError,
    CartNotFoundError,
)
from modules.cart.domain.factories.cart_factory import CartFactory
from modules.cart.infrastructure.models import CartModel, CartItemModel
from modules.cart.infrastructure.repositories.cart_repository import CartRepository


@pytest.mark.django_db
def test_create_cart_successfully() -> None:
    # Given: a user with cart data
    user_id = uuid4()
    data = {
        "user_id": user_id,
        "items": [
            {
                "product_id": uuid4(),
                "quantity": 2,
                "unit_price": "15.00",
            },
        ],
    }

    # When: the user creates a cart
    cart = CartFactory.from_dict(data)
    repo = CartRepository()
    result = repo.create(cart)

    # Then: a valid cart is returned with one item
    assert isinstance(result, Cart)
    assert result.user_id == user_id
    assert len(result.items) == 1


@pytest.mark.django_db
def test_create_cart_when_cart_already_exists_raises_error() -> None:
    # Given: a user who already has a cart
    user_id = uuid4()
    CartModel.objects.create(user_id=user_id)

    # When: the user tries to create a new cart
    cart = CartFactory.from_dict({"user_id": user_id, "items": []})
    repo = CartRepository()

    # Then: an error is raised indicating the cart already exists
    with pytest.raises(CartDomainError) as exc:
        repo.create(cart)

    assert "Cart already exists." in str(exc.value)


@pytest.mark.django_db
def test_get_cart_by_user_successful() -> None:
    # Given: a user with a cart and one item
    user_id = uuid4()
    cart = CartModel.objects.create(user_id=user_id)
    CartItemModel.objects.create(
        cart=cart,
        product_id=uuid4(),
        quantity=1,
        unit_price=Decimal("5.00"),
    )

    # When: the cart is retrieved by user
    repo = CartRepository()
    result = repo.get_by_user(user_id)

    # Then: the cart is returned with the expected item
    assert result.user_id == user_id
    assert len(result.items) == 1


@pytest.mark.django_db
def test_get_cart_by_user_not_found_raises_error() -> None:
    # Given: a user with no cart

    # When & Then: retrieving the cart raises CartNotFoundError
    repo = CartRepository()
    with pytest.raises(CartNotFoundError):
        repo.get_by_user(uuid4())


@pytest.mark.django_db
def test_patch_cart_item_quantity() -> None:
    # Given: a cart with one item
    user_id = uuid4()
    cart = CartModel.objects.create(user_id=user_id)
    item = CartItemModel.objects.create(
        cart=cart,
        product_id=uuid4(),
        quantity=1,
        unit_price=Decimal("5.00"),
    )

    # When: the item's quantity is updated
    repo = CartRepository()
    result = repo.patch_item(user_id=user_id, item_id=item.id, quantity=3)

    # Then: the item's quantity is updated successfully
    assert any(i.quantity.value == 3 for i in result.items)


@pytest.mark.django_db
def test_patch_item_not_found_raises_error() -> None:
    # Given: a user and an item ID that does not exist

    # When & Then: patching the item raises CartItemNotFoundError
    repo = CartRepository()
    with pytest.raises(CartItemNotFoundError):
        repo.patch_item(user_id=uuid4(), item_id=uuid4(), quantity=5)


@pytest.mark.django_db
def test_delete_cart_item_successful() -> None:
    # Given: a cart with one item
    user_id = uuid4()
    cart = CartModel.objects.create(user_id=user_id)
    item = CartItemModel.objects.create(
        cart=cart,
        product_id=uuid4(),
        quantity=1,
        unit_price=Decimal("2.00"),
    )

    # When: the item is deleted
    repo = CartRepository()
    result = repo.delete_item(user_id=user_id, item_id=item.id)

    # Then: the item is removed from the cart and the DB
    assert all(i.id != item.id for i in result.items)
    assert CartItemModel.objects.count() == 0


@pytest.mark.django_db
def test_delete_cart_item_not_found() -> None:
    # Given: a user and item ID that do not exist

    # When & Then: deleting the item raises CartItemNotFoundError
    repo = CartRepository()
    with pytest.raises(CartItemNotFoundError):
        repo.delete_item(user_id=uuid4(), item_id=uuid4())
