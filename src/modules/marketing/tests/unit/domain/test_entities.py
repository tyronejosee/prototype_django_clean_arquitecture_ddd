from datetime import datetime, timedelta, UTC
from decimal import Decimal
from uuid import uuid4

import pytest

from modules.marketing.domain.entities.coupon import Coupon
from modules.marketing.domain.entities.promotion import Promotion
from modules.marketing.domain.exceptions import CouponDomainError, PromotionDomainError
from modules.marketing.domain.value_objects.coupon_code import CouponCode
from modules.marketing.domain.value_objects.discount_percent import DiscountPercent

# --------------------------
# Coupon
# --------------------------


def build_valid_coupon(**overrides) -> Coupon:
    return Coupon(
        id=overrides.get("id", uuid4()),
        code=CouponCode("TEST123"),
        discount_percent=DiscountPercent(Decimal("0.2")),
        is_active=overrides.get("is_active", True),
        max_uses=overrides.get("max_uses", 5),
        used_count=overrides.get("used_count", 0),
        user_id=overrides.get("user_id", None),
        expires_at=overrides.get("expires_at", datetime.now(UTC) + timedelta(days=5)),
    )


def test_valid_coupon_passes_validation() -> None:
    # Given: a valid coupon
    coupon = build_valid_coupon()

    # Then: no error is raised and fields are set
    assert coupon.code.value == "TEST123"
    assert coupon.used_count == 0


def test_expired_coupon_raises_validation_error() -> None:
    # Given: a coupon with expiration in the past
    expires_at = datetime.now(UTC) - timedelta(days=1)

    # When & Then: should raise validation error
    with pytest.raises(CouponDomainError) as exc_info:
        build_valid_coupon(expires_at=expires_at)
    assert "Coupon has expired." in str(exc_info.value)


def test_negative_used_count_raises_validation_error() -> None:
    # Given: a coupon with negative usage count
    with pytest.raises(CouponDomainError) as exc_info:
        build_valid_coupon(used_count=-1)
    assert "Used count cannot be negative." in str(exc_info.value)


def test_coupon_max_usage_exceeded_raises_error() -> None:
    # Given: a coupon with max_uses reached
    with pytest.raises(CouponDomainError) as exc_info:
        build_valid_coupon(used_count=5)
    assert "Coupon is active but usage limit reached." in str(exc_info.value)


def test_coupon_is_valid_returns_true() -> None:
    # Given: a valid coupon and current datetime
    coupon = build_valid_coupon()
    now = datetime.now(UTC)

    # Then: is_valid returns True
    assert coupon.is_valid(now) is True


# --------------------------
# Promotion
# --------------------------


def build_valid_promotion(**overrides) -> Promotion:
    starts = overrides.get("starts_at", datetime.now(UTC))
    ends = overrides.get("ends_at", starts + timedelta(days=10))

    return Promotion(
        id=overrides.get("id", uuid4()),
        name=overrides.get("name", "Summer Sale"),
        description=overrides.get("description", "10% off everything."),
        discount_percent=DiscountPercent(Decimal("0.1")),
        is_active=overrides.get("is_active", True),
        starts_at=starts,
        ends_at=ends,
    )


def test_valid_promotion_passes_validation() -> None:
    # Given: a promotion with a valid configuration
    promo = build_valid_promotion()

    # Then: its attributes should be correctly set
    assert promo.name == "Summer Sale"
    assert promo.discount_percent.value == Decimal("0.1")


@pytest.mark.parametrize("name", ["", "   "])
def test_promotion_with_blank_name_raises_error(name: str) -> None:
    # Given: an invalid name (blank or whitespace)

    # When: creating a promotion with the invalid name
    with pytest.raises(PromotionDomainError) as exc_info:
        build_valid_promotion(name=name)

    # Then: an appropriate domain error should be raised
    assert "Promotion name is required." in str(exc_info.value)


def test_promotion_end_before_start_raises_error() -> None:
    # Given: a start date and an end date before it
    starts = datetime.now(UTC)
    ends = starts - timedelta(days=1)

    # When: creating a promotion with these dates
    with pytest.raises(PromotionDomainError) as exc_info:
        build_valid_promotion(starts_at=starts, ends_at=ends)

    # Then: an error should be raised due to invalid range
    assert "Promotion end date must be after the start date." in str(exc_info.value)


@pytest.mark.parametrize("duration_days", [1, 100])
def test_promotion_duration_invalid_range_raises_error(duration_days: int) -> None:
    # Given: a promotion with a duration of X days (too short or too long)
    starts = datetime.now(UTC)
    ends = starts + timedelta(days=duration_days)

    # When & Then: trying to create the promotion should raise an error
    with pytest.raises(PromotionDomainError):
        build_valid_promotion(starts_at=starts, ends_at=ends)


def test_promotion_ending_in_past_raises_error() -> None:
    # Given: an end date in the past
    ends = datetime.now(UTC) - timedelta(days=1)

    # When: creating a promotion that ends in the past
    with pytest.raises(PromotionDomainError) as exc_info:
        build_valid_promotion(ends_at=ends)

    # Then: an error should be raised
    assert "Promotion end date must be after the start date." in str(exc_info.value)


def test_promotion_start_too_far_in_future_raises_error() -> None:
    # Given: a start date far in the future
    starts = datetime.now(UTC) + timedelta(days=365 * 6)

    # When: creating a promotion starting that far ahead
    with pytest.raises(PromotionDomainError) as exc_info:
        build_valid_promotion(starts_at=starts)

    # Then: an error should be raised
    assert "Promotion start date is too far in the future." in str(exc_info.value)


def test_promotion_description_too_long_raises_error() -> None:
    # Given: a description longer than allowed
    long_description = "A" * 300

    # When: creating a promotion with it
    with pytest.raises(PromotionDomainError) as exc_info:
        build_valid_promotion(description=long_description)

    # Then: an error should be raised
    assert "Promotion description is too long." in str(exc_info.value)


def test_promotion_is_valid_returns_true_when_active_and_within_dates() -> None:
    # Given: an active promotion within the valid date range
    promo = build_valid_promotion()
    now = datetime.now(UTC)

    # When: checking its validity
    result = promo.is_valid(now)

    # Then: it should be valid
    assert result is True


def test_promotion_is_valid_returns_false_when_inactive_or_outside_dates() -> None:
    # Given: time references
    future = datetime.now(UTC) + timedelta(days=10)
    past = datetime.now(UTC) - timedelta(days=10)
    now = datetime.now(UTC)

    # When: promotion is inactive
    inactive = build_valid_promotion(is_active=False)
    # Then: it should not be valid
    assert inactive.is_valid(now) is False

    # When: promotion has not started yet
    not_yet_started = build_valid_promotion(
        starts_at=future,
        ends_at=future + timedelta(days=10),
    )
    # Then: it should not be valid
    assert not_yet_started.is_valid(now) is False

    # When: promotion ends in the past
    # Then: error should be raised during construction
    with pytest.raises(PromotionDomainError) as exc_info:
        build_valid_promotion(starts_at=past - timedelta(days=10), ends_at=past)
    assert "Promotion cannot end in the past." in str(exc_info.value)
