from decimal import Decimal

import pytest

from src.modules.marketing.domain.exceptions import CouponDomainError, MarketingDomainError
from src.modules.marketing.domain.value_objects.coupon_code import CouponCode
from src.modules.marketing.domain.value_objects.discount_percent import DiscountPercent
from src.modules.marketing.domain.value_objects.discount_result import DiscountResult


class TestCouponCode:
    def test_creates_successfully_with_valid_code(self) -> None:
        # Given: a valid coupon code
        code = "ABC123XYZ"

        # When: creating the CouponCode
        result = CouponCode(code)

        # Then: it should store the value
        assert result.value == code

    @pytest.mark.parametrize("code", ["", None])
    def test_raises_error_when_code_missing(self, code: str | None) -> None:
        # Given: an empty or missing code
        # When & Then: should raise validation error
        with pytest.raises(CouponDomainError, match="required"):
            CouponCode(code)  # type: ignore

    @pytest.mark.parametrize("code", ["abc", "TOO_LONG_CODE_1234567890", "INVALID*CODE"])
    def test_raises_error_when_code_invalid(self, code: str) -> None:
        # Given: an invalid code format or length
        # When & Then: should raise validation error
        with pytest.raises(CouponDomainError):
            CouponCode(code)


class TestDiscountPercent:
    @pytest.mark.parametrize("percent", [Decimal("0.1"), Decimal("0.5")])
    def test_accepts_valid_percent(self, percent: Decimal) -> None:
        # Given: a valid percent
        dp = DiscountPercent(percent)
        assert dp.value == percent

    @pytest.mark.parametrize("percent", [Decimal("0"), Decimal("0.6"), Decimal("-0.1")])
    def test_raises_error_when_percent_invalid(self, percent: Decimal) -> None:
        # Given: an invalid discount
        # When & Then: should raise domain error
        with pytest.raises(MarketingDomainError, match="invalid"):
            DiscountPercent(percent)

    def test_discount_result_stores_expected_fields(self) -> None:
        # Given: a final price and list of messages
        result = DiscountResult(
            final_price=Decimal("99.99"),
            applied_discounts=["Promo A", "Coupon B"],
        )

        # Then: all fields are stored correctly
        assert result.final_price == Decimal("99.99")
        assert result.applied_discounts == ["Promo A", "Coupon B"]
