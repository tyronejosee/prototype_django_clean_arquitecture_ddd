import pytest

from src.modules.cart.domain.exceptions import CartDomainError
from src.modules.cart.domain.value_objects.item_quantity import ItemQuantity


class TestItemQuantity:
    def test_valid_quantity(self) -> None:
        # Given: a valid quantity value
        valid_value = 5

        # When: creating an ItemQuantity with that value
        quantity = ItemQuantity(valid_value)

        # Then: the internal value equals the given valid value
        assert quantity.value == valid_value

    @pytest.mark.parametrize("invalid_value", [0, 11, -1, 100])
    def test_quantity_out_of_range_raises_error(self, invalid_value: int) -> None:
        # Given: an invalid quantity value outside the accepted range

        # When & Then: creating an ItemQuantity raises a CartDomainError
        with pytest.raises(CartDomainError) as exc_info:
            ItemQuantity(invalid_value)

        assert "Quantity must be between" in str(exc_info.value)
