from uuid import uuid4

import pytest

from src.modules.cart.domain.entities.cart import Cart
from src.modules.cart.domain.exceptions import CartDomainError, CartItemNotFoundError, CartNotFoundError
from src.modules.cart.infrastructure.models import CartItemModel, CartModel
from src.modules.cart.infrastructure.repositories.cart_repository import CartRepository


@pytest.mark.django_db()
class TestCartRepository:
    def test_create_cart_successfully(self) -> None:
        # Given: a user
        user_id = uuid4()

        # When: the user creates a cart
        repo = CartRepository()
        result = repo.create(user_id=user_id)

        # Then: a valid cart is returned
        assert isinstance(result, Cart)
        assert result.user_id == user_id

    def test_create_cart_when_cart_already_exists_raises_error(self) -> None:
        # Given: a user who already has a cart
        user_id = uuid4()
        CartModel.objects.create(user_id=user_id)
        repo = CartRepository()

        # When: the user tries to create a new cart
        with pytest.raises(CartDomainError) as exc:
            repo.create(user_id=user_id)

        # Then: an error is raised indicating the cart already exists
        assert "Cart already exists." in str(exc.value)

    def test_get_cart_by_user_successful(self) -> None:
        # Given: a user with a cart and one item
        user_id = uuid4()
        cart = CartModel.objects.create(user_id=user_id)
        CartItemModel.objects.create(
            cart_id=cart,
            product_id=uuid4(),
            quantity=1,
        )

        # When: the cart is retrieved by user
        repo = CartRepository()
        result = repo.get_by_user(user_id)

        # Then: the cart is returned with the expected item
        assert result.user_id == user_id
        assert len(result.items) == 1  # type: ignore[union-attr]

    def test_get_cart_by_user_not_found_raises_error(self) -> None:
        # Given: a user with no cart

        # When & Then: retrieving the cart raises CartNotFoundError
        repo = CartRepository()
        with pytest.raises(CartNotFoundError):
            repo.get_by_user(uuid4())

    def test_patch_cart_item_quantity(self) -> None:
        # Given: a cart with one item
        user_id = uuid4()
        cart = CartModel.objects.create(user_id=user_id)
        item = CartItemModel.objects.create(cart_id=cart, product_id=uuid4(), quantity=1)

        # When: the item's quantity is updated
        repo = CartRepository()
        result = repo.patch_item(user_id=user_id, item_id=item.id, quantity=3)

        # Then: the item's quantity is updated successfully
        assert any(i.quantity.value == 3 for i in result.items)  # type: ignore[union-attr]

    def test_patch_item_not_found_raises_error(self) -> None:
        # Given: a user and an item ID that does not exist

        # When & Then: patching the item raises CartItemNotFoundError
        repo = CartRepository()
        with pytest.raises(CartItemNotFoundError):
            repo.patch_item(user_id=uuid4(), item_id=uuid4(), quantity=5)

    def test_delete_cart_item_successful(self) -> None:
        # Given: a cart with one item
        user_id = uuid4()
        cart = CartModel.objects.create(user_id=user_id)
        item = CartItemModel.objects.create(cart_id=cart, product_id=uuid4(), quantity=1)

        # When: the item is deleted
        repo = CartRepository()
        repo.delete_item(user_id=user_id, item_id=item.id)

        # Then:
        assert CartItemModel.objects.count() == 0
        assert not CartItemModel.objects.filter(id=item.id).exists()

    def test_delete_cart_item_not_found(self) -> None:
        # Given: a user and item ID that do not exist

        # When & Then: deleting the item raises CartItemNotFoundError
        repo = CartRepository()
        with pytest.raises(CartItemNotFoundError):
            repo.delete_item(user_id=uuid4(), item_id=uuid4())
