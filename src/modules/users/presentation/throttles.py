from rest_framework.throttling import UserRateThrottle

from src.core.settings import THROTTLE_10_PER_MINUTE


class ListWishlistRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class AddWhishlistItemRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class DeleteWhishlistItemRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE
