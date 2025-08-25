from unittest.mock import Mock
from uuid import uuid4

from src.modules.cart.application.use_cases.add_cart_items import AddCartItemsUseCase
from src.modules.cart.application.use_cases.create_cart import CreateCartUseCase
from src.modules.cart.application.use_cases.delete_cart_item import DeleteCartItemUseCase
from src.modules.cart.application.use_cases.get_cart import GetCartUseCase
from src.modules.cart.application.use_cases.patch_cart_item import PatchCartItemUseCase
from src.modules.cart.domain.entities.cart import Cart
from src.modules.cart.domain.factories.cart_factory import CartFactory
from src.modules.cart.domain.utils.cart_cache_keys import CartCacheKeys
from src.modules.cart.domain.value_objects.item_quantity import ItemQuantity


class TestAddCartItemsUseCase:
    def test_add_cart_items_successfully(self) -> None:
        # Given: repo mocks and cache, user_id and items data to add
        repo_mock = Mock()
        cache_mock = Mock()
        user_id = uuid4()
        items_payload: dict = {
            "items": [{"product_id": str(uuid4()), "quantity": 5}, {"product_id": str(uuid4()), "quantity": 2}]
        }
        expected_cart = Mock(spec=Cart)
        repo_mock.add_items.return_value = expected_cart
        product_catalog_mock = Mock()

        # When: executing the use case with the data
        use_case = AddCartItemsUseCase(repo=repo_mock, cache=cache_mock, product_catalog=product_catalog_mock)
        result = use_case.execute(user_id=user_id, items_data=items_payload["items"])

        # Then: the result is the expected cart
        assert result == expected_cart
        repo_mock.add_items.assert_called_once()
        called_args = repo_mock.add_items.call_args[1]
        assert called_args["user_id"] == user_id
        assert len(called_args["items"]) == len(items_payload["items"])
        cache_mock.delete.assert_called_once_with(CartCacheKeys.cart_user_key(user_id))


class TestCreateCartUseCase:
    def test_create_cart_successfully(self) -> None:
        # Given: a repository mock and cart data for a user
        repo_mock = Mock()
        user_id = uuid4()
        cart_data = {"user_id": user_id, "items": []}
        expected_cart = CartFactory.from_dict(cart_data)
        repo_mock.create.return_value = expected_cart

        # When: creating a cart use case and executing with the data
        use_case = CreateCartUseCase(repo=repo_mock)
        result = use_case.execute(user_id=user_id)

        # Then: the result is a Cart with the correct user_id and repo.create called once
        assert isinstance(result, Cart)
        assert result.user_id == user_id
        repo_mock.create.assert_called_once()


class TestGetCartUseCase:
    def test_get_cart_successfully(self) -> None:
        # Given: a repo mock configured to return a cart for a user_id
        repo_mock = Mock()
        cache_mock = Mock()
        user_id = uuid4()
        expected_cart = Mock(spec=Cart)
        cache_mock.get.return_value = expected_cart

        # When: calling GetCartUseCase with that user_id
        use_case = GetCartUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute(user_id)

        # Then: the returned cart matches expected and repo method called properly
        assert result == expected_cart
        cache_mock.get.assert_called_once()
        repo_mock.get_by_user.assert_not_called()
        cache_mock.get.assert_called_once_with(CartCacheKeys.cart_user_key(user_id))


class TestPatchCartItemUseCase:
    def test_patch_cart_item_successfully(self) -> None:
        # Given: a repo mock, cache mock, user_id, item_id, and quantity to patch
        repo_mock = Mock()
        cache_mock = Mock()
        user_id = uuid4()
        item_id = uuid4()
        quantity = ItemQuantity(3)
        expected_cart = Mock(spec=Cart)
        repo_mock.patch_item.return_value = expected_cart

        # When: patching cart item via use case
        use_case = PatchCartItemUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute(user_id, item_id, quantity)

        # Then: returned cart matches expected and repo.patch_item called with expected args
        assert result == expected_cart
        repo_mock.patch_item.assert_called_once_with(user_id=user_id, item_id=item_id, quantity=3)
        cache_mock.delete.assert_called_once_with(CartCacheKeys.cart_user_key(user_id))


class TestDeleteCartItemUseCase:
    def test_delete_cart_item_successfully(self) -> None:
        # Given: a repo mock, cache mock, user_id and item_id to delete
        repo_mock = Mock()
        cache_mock = Mock()
        user_id = uuid4()
        item_id = uuid4()

        # When: deleting cart item via use case
        use_case = DeleteCartItemUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute(user_id=user_id, item_id=item_id)

        # Then: nothing is returned
        assert result is None

        # And: dependencies were called correctly
        repo_mock.delete_item.assert_called_once_with(user_id=user_id, item_id=item_id)
        cache_mock.delete.assert_called_once_with(CartCacheKeys.cart_user_key(user_id))
