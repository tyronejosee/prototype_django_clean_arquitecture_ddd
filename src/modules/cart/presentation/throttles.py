from rest_framework.throttling import UserRateThrottle

from src.core.settings import THROTTLE_5_PER_MINUTE


class ListCartRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_5_PER_MINUTE


class CreateCartRateThrottle(UserRateThrottle):
    rate: str = "2/day"


class AddCartItemsRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_5_PER_MINUTE


class UpdateCartItemRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_5_PER_MINUTE


class DeleteCartItemRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_5_PER_MINUTE
