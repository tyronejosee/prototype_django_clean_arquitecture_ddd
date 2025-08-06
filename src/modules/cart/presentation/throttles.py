from rest_framework.throttling import UserRateThrottle

from src.core.settings import THROTTLE_2_PER_DAY, THROTTLE_10_PER_MINUTE


class ListCartRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class CreateCartRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_2_PER_DAY


class AddCartItemsRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class UpdateCartItemRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class DeleteCartItemRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE
