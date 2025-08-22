from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from src.modules.marketing.domain.entities.coupon import Coupon
from src.modules.marketing.domain.entities.promotion import Promotion
from src.modules.marketing.domain.exceptions import CouponNotFoundError
from src.modules.marketing.domain.value_objects.coupon_code import CouponCode
from src.modules.marketing.domain.value_objects.discount_percent import DiscountPercent
from src.modules.marketing.infrastructure.models.coupon_model import CouponModel
from src.modules.marketing.infrastructure.repositories.coupon_repository import CouponRepository
from src.modules.marketing.infrastructure.repositories.promotion_repository import PromotionRepository


@pytest.mark.django_db()
class TestCouponRepository:
    def test_should_create_and_retrieve_coupon(self) -> None:
        # Given: a valid Coupon entity to be persisted
        repo = CouponRepository()
        coupon = Coupon(
            id=uuid4(),
            code=CouponCode("ABC123"),
            discount_percent=DiscountPercent(Decimal("0.1")),
            is_active=True,
            max_uses=5,
            used_count=1,
            user_id=None,
            expires_at=datetime.now(UTC) + timedelta(days=5),
        )

        # When: the coupon is created using the repository
        saved = repo.create(coupon)

        # Then: the saved coupon should match the input data
        assert isinstance(saved, Coupon)
        assert saved.id == coupon.id
        assert saved.code == coupon.code

    def test_should_return_true_only_when_coupon_exists_by_code(self) -> None:
        # Given: a coupon already saved in the DB
        CouponModel.objects.create(
            code="EXIST123",
            discount_percent=Decimal("0.1"),
            is_active=True,
            expires_at=datetime.now(UTC) + timedelta(days=5),
        )
        repo = CouponRepository()

        # When & Then: checking existence by code should return correct boolean
        assert repo.exists_by_code("EXIST123") is True
        assert repo.exists_by_code("NONEXIST") is False

    def test_should_return_coupon_when_code_exists(self) -> None:
        # Given: a coupon stored with a known code
        CouponModel.objects.create(
            code="MYCODE",
            discount_percent=Decimal("0.1"),
            is_active=True,
            expires_at=datetime.now(UTC) + timedelta(days=3),
        )
        repo = CouponRepository()

        # When: fetching the coupon by its code
        coupon = repo.get_by_code("MYCODE")

        # Then: the coupon is returned and matches the code
        assert isinstance(coupon, Coupon)
        assert coupon.code == "MYCODE"

    def test_should_raise_error_when_coupon_not_found_by_code(self) -> None:
        # Given: no coupon exists with the given code
        repo = CouponRepository()

        # When & Then: attempting to get it should raise CouponNotFoundError
        with pytest.raises(CouponNotFoundError):
            repo.get_by_code("UNKNOWN")

    def test_should_return_only_active_coupons_for_user(self) -> None:
        # Given: a user with a mix of active and inactive/expired coupons
        user_id = uuid4()

        # Active and available
        CouponModel.objects.create(
            code="A1",
            discount_percent=Decimal("0.1"),
            is_active=True,
            user_id=user_id,
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )

        # Expired (but still marked active)
        CouponModel.objects.create(
            code="A2",
            discount_percent=Decimal("0.1"),
            is_active=False,
            user_id=user_id,
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )

        # Inactive
        CouponModel.objects.create(
            code="A3",
            discount_percent=Decimal("0.1"),
            is_active=False,
            user_id=user_id,
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )

        repo = CouponRepository()

        # When: retrieving active coupons for the user
        results = repo.get_active_by_user(user_id)

        # Then: only the active coupon should be returned
        assert len(results) == 1
        assert results[0].code == "A1"


@pytest.mark.django_db()
class TestPromotionRepository:
    def test_should_create_promotions_and_return_only_active(self) -> None:
        # Given: two promotions, one active and one inactive
        repo = PromotionRepository()

        active = Promotion(
            id=uuid4(),
            name="Back to School",
            description="10% off",
            discount_percent=DiscountPercent(Decimal("0.1")),
            is_active=True,
            starts_at=datetime.now(UTC),
            ends_at=datetime.now(UTC) + timedelta(days=10),
        )

        inactive = Promotion(
            id=uuid4(),
            name="Old Promo",
            description="no longer active",
            discount_percent=DiscountPercent(Decimal("0.1")),
            is_active=False,
            starts_at=datetime.now(UTC),
            ends_at=datetime.now(UTC) + timedelta(days=10),
        )

        repo.create(active)
        repo.create(inactive)

        # When: querying for active promotions
        results = repo.get_active()
        names = [p.name for p in results]

        # Then: only the active promotion should be returned
        assert "Back to School" in names
        assert "Old Promo" not in names
