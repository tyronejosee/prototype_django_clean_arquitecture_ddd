from unittest.mock import Mock
from uuid import uuid4

from apps.cart.application.use_cases.create_cart import CreateCartUseCase
from apps.cart.application.use_cases.delete_cart_item import DeleteCartItemUseCase
from apps.cart.application.use_cases.get_cart import GetCartUseCase
from apps.cart.application.use_cases.patch_cart_item import PatchCartItemUseCase
from apps.cart.application.use_cases.preview_cart import PreviewCartUseCase
from apps.cart.application.use_cases.update_cart import UpdateCartUseCase
from apps.cart.domain.entities.cart import Cart
from apps.cart.domain.factories.cart_factory import CartFactory
from apps.cart.domain.value_objects.item_quantity import ItemQuantity


def test_create_cart_successful() -> None:
    # Given: a repository mock and cart data for a user
    repo_mock = Mock()
    user_id = uuid4()
    cart_data = {
        "user_id": user_id,
        "items": [],
    }
    expected_cart = CartFactory.from_dict(cart_data)
    repo_mock.create.return_value = expected_cart

    # When: creating a cart use case and executing with the data
    use_case = CreateCartUseCase(repo=repo_mock)
    result = use_case.execute(cart_data)

    # Then: the result is a Cart with the correct user_id and repo.create called once
    assert isinstance(result, Cart)
    assert result.user_id == user_id
    repo_mock.create.assert_called_once()


def test_get_cart_by_user_successful() -> None:
    # Given: a repo mock configured to return a cart for a user_id
    repo_mock = Mock()
    user_id = uuid4()
    expected_cart = Mock(spec=Cart)
    repo_mock.get_by_user.return_value = expected_cart

    # When: calling GetCartUseCase with that user_id
    use_case = GetCartUseCase(repo=repo_mock)
    result = use_case.execute(user_id)

    # Then: the returned cart matches expected and repo method called properly
    assert result == expected_cart
    repo_mock.get_by_user.assert_called_once_with(user_id=user_id)


def test_update_cart_successful() -> None:
    # Given: a repo mock and cart data for update
    repo_mock = Mock()
    user_id = uuid4()
    cart_data = {
        "user_id": user_id,
        "items": [],
    }
    expected_cart = CartFactory.from_dict(cart_data)
    repo_mock.update.return_value = expected_cart

    # When: executing update cart use case
    use_case = UpdateCartUseCase(repo=repo_mock)
    result = use_case.execute(cart_data)

    # Then: result is Cart with correct user_id and repo.update called once
    assert isinstance(result, Cart)
    assert result.user_id == user_id
    repo_mock.update.assert_called_once()


def test_patch_cart_item_successful() -> None:
    # Given: a repo mock, user_id, item_id, and quantity to patch
    repo_mock = Mock()
    user_id = uuid4()
    item_id = uuid4()
    quantity = ItemQuantity(3)
    expected_cart = Mock(spec=Cart)
    repo_mock.patch_item.return_value = expected_cart

    # When: patching cart item via use case
    use_case = PatchCartItemUseCase(repo=repo_mock)
    result = use_case.execute(user_id, item_id, quantity)

    # Then: returned cart matches expected and repo.patch_item called with expected args
    assert result == expected_cart
    repo_mock.patch_item.assert_called_once_with(
        user_id=user_id, item_id=item_id, quantity=3
    )


def test_delete_cart_item_successful() -> None:
    # Given: a repo mock, user_id and item_id to delete
    repo_mock = Mock()
    user_id = uuid4()
    item_id = uuid4()
    expected_cart = Mock(spec=Cart)
    repo_mock.delete_item.return_value = expected_cart

    # When: deleting cart item via use case
    use_case = DeleteCartItemUseCase(repo=repo_mock)
    result = use_case.execute(user_id=user_id, item_id=item_id)

    # Then: returned cart matches expected and
    # repo.delete_item called once with correct args
    assert result == expected_cart
    repo_mock.delete_item.assert_called_once_with(user_id=user_id, item_id=item_id)


def test_preview_cart_returns_expected_dict() -> None:
    # Given: a repo mock and cart data for preview
    repo_mock = Mock()
    cart_data = {
        "user_id": "user123",
        "items": [],
    }
    expected_preview = {
        "subtotal": 100,
        "taxes": 19,
        "total": 119,
    }
    repo_mock.preview.return_value = expected_preview

    # When: executing preview cart use case
    use_case = PreviewCartUseCase(repo=repo_mock)
    result = use_case.execute(cart_data)

    # Then: returned dict matches expected and
    # repo.preview called once with cart data
    assert result == expected_preview
    repo_mock.preview.assert_called_once_with(cart_data)
