from datetime import UTC, datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

import pytest

from src.modules.marketing.application.use_cases.apply_discounts import ApplyDiscountsUseCase
from src.modules.marketing.application.use_cases.create_coupon import CreateCouponUseCase
from src.modules.marketing.application.use_cases.create_promotion import CreatePromotionUseCase
from src.modules.marketing.application.use_cases.get_active_coupons import GetActiveCouponsUseCase
from src.modules.marketing.application.use_cases.get_active_promotions import GetActivePromotionsUseCase
from src.modules.marketing.domain.entities.coupon import Coupon
from src.modules.marketing.domain.entities.promotion import Promotion
from src.modules.marketing.domain.exceptions import CouponDomainError


class TestApplyDiscountsUseCase:
    def test_returns_discount_result_when_handler_applies(self) -> None:
        # Given: a mock discount handler that returns a fixed result
        handler = Mock()
        handler.apply.return_value = Mock(
            final_price=Decimal("80.00"),
            applied_discounts=["10% OFF"],
        )
        use_case = ApplyDiscountsUseCase(chain=handler)

        # When: executing the use case with a sample order
        result = use_case.execute(order={"total": Decimal("100.00")})

        # Then: the discount result should match the handler's return value
        assert result["final_price"] == Decimal("80.00")
        assert result["applied_discounts"] == ["10% OFF"]
        handler.apply.assert_called_once()


class TestCreateCouponUseCase:
    def test_creates_coupon_with_valid_data(self) -> None:
        # Given: a repository that does not find the given code
        repo = Mock()
        repo.exists_by_code.return_value = False
        repo.create.side_effect = lambda c: c

        data = {
            "code": "HELLO10",
            "discount_percent": Decimal("0.1"),
            "expires_at": datetime.now(UTC) + timedelta(days=10),
        }
        use_case = CreateCouponUseCase(coupon_repo=repo)

        # When: executing the use case with valid input
        coupon = use_case.execute(data)

        # Then: a valid coupon instance is returned and saved
        assert isinstance(coupon, Coupon)
        assert coupon.code.value == "HELLO10"
        repo.create.assert_called_once()

    def test_raises_error_when_code_already_exists(self) -> None:
        # Given: a repository that finds an existing coupon with the same code
        repo = Mock()
        repo.exists_by_code.return_value = True
        use_case = CreateCouponUseCase(coupon_repo=repo)

        # When & Then: attempting to create a coupon with duplicate code raises an error
        with pytest.raises(CouponDomainError, match="already exists"):
            use_case.execute(
                {
                    "code": "DUPLICATE",
                    "discount_percent": Decimal("0.1"),
                    "expires_at": datetime.now(UTC),
                }
            )

    def test_generates_code_when_missing(self) -> None:
        # Given: a repository that accepts new coupons and a request with no code
        repo = Mock()
        repo.exists_by_code.return_value = False
        repo.create.side_effect = lambda c: c

        use_case = CreateCouponUseCase(coupon_repo=repo)
        data = {
            "code": "",
            "discount_percent": Decimal("0.1"),
            "expires_at": datetime.now(UTC) + timedelta(days=10),
        }

        # When: executing the use case
        coupon = use_case.execute(data)

        # Then: a code is generated and the coupon is valid
        assert isinstance(coupon.code.value, str)
        assert 4 <= len(coupon.code.value) <= 20


class TestCreatePromotionUseCase:
    def test_creates_promotion_with_valid_data(self) -> None:
        # Given: a promotion repo that accepts new promotions
        repo = Mock()
        repo.create.side_effect = lambda p: p

        data = {
            "name": "Flash Sale",
            "description": "Quick 2-day sale",
            "discount_percent": Decimal("0.1"),
            "starts_at": datetime.now(UTC),
            "ends_at": datetime.now(UTC) + timedelta(days=10),
        }
        use_case = CreatePromotionUseCase(promotion_repo=repo)

        # When: executing the use case
        promo = use_case.execute(data)

        # Then: a promotion is created and persisted
        assert isinstance(promo, Promotion)
        assert promo.name == "Flash Sale"
        repo.create.assert_called_once()


class TestGetActiveCouponsUseCase:
    def test_returns_active_coupons_for_user(self) -> None:
        # Given: a repo that returns a list of active coupons
        repo = Mock()
        repo.get_active_by_user.return_value = ["coupon1", "coupon2"]
        use_case = GetActiveCouponsUseCase(coupon_repo=repo)

        user_id = uuid4()

        # When: executing the use case with a user ID
        result = use_case.execute(user_id=user_id)

        # Then: the list of active coupons is returned
        assert result == ["coupon1", "coupon2"]
        repo.get_active_by_user.assert_called_once_with(user_id)


class TestGetActivePromotionsUseCase:
    def test_returns_active_promotions(self) -> None:
        # Given: a repo that returns a list of active promotions
        repo = Mock()
        repo.get_active.return_value = ["promo1", "promo2"]
        use_case = GetActivePromotionsUseCase(promotion_repo=repo)

        # When: executing the use case
        result = use_case.execute()

        # Then: the list of active promotions is returned
        assert result == ["promo1", "promo2"]
        repo.get_active.assert_called_once()
