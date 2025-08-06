from unittest.mock import patch, Mock
from uuid import uuid4

import pytest

from src.modules.cart.domain.factories.cart_item_factory import CartItemFactory
from src.modules.cart.infrastructure.models.cart_model import CartModel
from src.modules.cart.infrastructure.services.cart_item_merge_service import CartItemMergerService


@pytest.fixture
def cart_model_mock() -> Mock:
    cart = Mock(spec=CartModel)
    cart._state = Mock()  # Model requires this to be set
    cart.items.all = Mock()
    return cart


class TestCartItemMergerService:
    @patch("src.modules.cart.infrastructure.models.CartItemModel.objects.bulk_create")
    @patch("src.modules.cart.infrastructure.models.CartItemModel.objects.bulk_update")
    def test_add_or_merge_only_creates(
        self, mock_bulk_update: Mock, mock_bulk_create: Mock, cart_model_mock: Mock
    ) -> None:
        # Given: no existing items in cart
        cart_model_mock.items.all.return_value = []

        # And: new items via factory
        new_items_data = [
            {"product_id": uuid4(), "quantity": 1},
            {"product_id": uuid4(), "quantity": 2},
        ]
        new_items = [CartItemFactory.from_dict(data) for data in new_items_data]

        # When: adding new items to cart
        CartItemMergerService.add_or_merge_items(cart_model=cart_model_mock, new_items=new_items)

        # Then: new items are created
        mock_bulk_create.assert_called_once()
        mock_bulk_update.assert_not_called()

    @patch("src.modules.cart.infrastructure.models.CartItemModel.objects.bulk_create")
    @patch("src.modules.cart.infrastructure.models.CartItemModel.objects.bulk_update")
    def test_add_or_merge_only_updates(
        self, mock_bulk_update: Mock, mock_bulk_create: Mock, cart_model_mock: Mock
    ) -> None:
        # Given: existing items matching the incoming product_ids
        product_id_1 = uuid4()
        product_id_2 = uuid4()

        existing_item_1 = Mock(product_id=product_id_1)
        existing_item_2 = Mock(product_id=product_id_2)
        cart_model_mock.items.all.return_value = [existing_item_1, existing_item_2]

        new_items_data = [
            {"product_id": product_id_1, "quantity": 5},
            {"product_id": product_id_2, "quantity": 3},
        ]
        new_items = [CartItemFactory.from_dict(data) for data in new_items_data]

        # When: adding new items to cart
        CartItemMergerService.add_or_merge_items(cart_model=cart_model_mock, new_items=new_items)

        # Then: existing items are updated
        mock_bulk_update.assert_called_once()
        mock_bulk_create.assert_not_called()
        assert existing_item_1.quantity == 5
        assert existing_item_2.quantity == 3

    @patch("src.modules.cart.infrastructure.models.CartItemModel.objects.bulk_create")
    @patch("src.modules.cart.infrastructure.models.CartItemModel.objects.bulk_update")
    def test_add_or_merge_mixed_create_and_update(
        self, mock_bulk_update: Mock, mock_bulk_create: Mock, cart_model_mock: Mock
    ) -> None:
        # Given: one existing and one new item
        existing_product_id = uuid4()
        new_product_id = uuid4()

        existing_item = Mock(product_id=existing_product_id)
        cart_model_mock.items.all.return_value = [existing_item]

        new_items_data = [
            {"product_id": existing_product_id, "quantity": 7},
            {"product_id": new_product_id, "quantity": 2},
        ]
        new_items = [CartItemFactory.from_dict(data) for data in new_items_data]

        # When: adding new items to cart
        CartItemMergerService.add_or_merge_items(cart_model=cart_model_mock, new_items=new_items)

        # Then: existing item is updated and new item is created
        mock_bulk_create.assert_called_once()
        mock_bulk_update.assert_called_once()
        assert existing_item.quantity == 7
