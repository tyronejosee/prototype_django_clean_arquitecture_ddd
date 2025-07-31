from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from modules.marketing.domain.exceptions import PromotionDomainError
from modules.marketing.domain.value_objects.discount_percent import DiscountPercent


@dataclass(kw_only=True, slots=True)
class Promotion:
    id: UUID
    name: str
    description: str
    discount_percent: DiscountPercent
    is_active: bool
    starts_at: datetime
    ends_at: datetime

    # Constants
    MAX_DESCRIPTION_LENGTH: int = 255

    # Messages
    PROMOTION_NAME_REQUIRED_ERROR_MSG: str = "Promotion name is required."
    PROMOTION_INVALID_DATE_RANGE_ERROR_MSG: str = "Promotion end date must be after the start date."
    PROMOTION_DURATION_TOO_SHORT_ERROR_MSG: str = "Promotion duration is too short."
    PROMOTION_DURATION_TOO_LONG_ERROR_MSG: str = "Promotion duration exceeds the maximum allowed."
    PROMOTION_ENDS_IN_PAST_ERROR_MSG: str = "Promotion cannot end in the past."
    PROMOTION_STARTS_TOO_FAR_ERROR_MSG: str = "Promotion start date is too far in the future."
    PROMOTION_DESCRIPTION_TOO_LONG_ERROR_MSG: str = "Promotion description is too long."

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        now = datetime.now(tz=self.starts_at.tzinfo)
        duration = self.ends_at - self.starts_at

        if not self.name.strip():
            raise PromotionDomainError(self.PROMOTION_NAME_REQUIRED_ERROR_MSG)

        if self.ends_at <= self.starts_at:
            raise PromotionDomainError(self.PROMOTION_INVALID_DATE_RANGE_ERROR_MSG)

        if duration < timedelta(days=7):
            raise PromotionDomainError(self.PROMOTION_DURATION_TOO_SHORT_ERROR_MSG)

        if duration > timedelta(days=30):
            raise PromotionDomainError(self.PROMOTION_DURATION_TOO_LONG_ERROR_MSG)

        if self.ends_at < now:
            raise PromotionDomainError(self.PROMOTION_ENDS_IN_PAST_ERROR_MSG)

        if self.starts_at > now + timedelta(days=365 * 5):
            raise PromotionDomainError(self.PROMOTION_STARTS_TOO_FAR_ERROR_MSG)

        if len(self.description) > self.MAX_DESCRIPTION_LENGTH:
            raise PromotionDomainError(self.PROMOTION_DESCRIPTION_TOO_LONG_ERROR_MSG)

    def is_valid(self, now: datetime) -> bool:
        return self.is_active and self.starts_at <= now <= self.ends_at
