from rest_framework.throttling import UserRateThrottle

from src.core.settings import THROTTLE_5_PER_HOUR, THROTTLE_10_PER_MINUTE


class RegisterRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_5_PER_HOUR


class LoginRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_5_PER_HOUR


class RefreshRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class TokenVerifyRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_5_PER_HOUR


class LogoutRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_5_PER_HOUR


class ListUsersRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class GetUserRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class UpdateUserRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_5_PER_HOUR


class DeleteUserRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_5_PER_HOUR


class CreateUserRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_5_PER_HOUR


class ListWishlistRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class AddWishlistItemRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class DeleteWishlistItemRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE
