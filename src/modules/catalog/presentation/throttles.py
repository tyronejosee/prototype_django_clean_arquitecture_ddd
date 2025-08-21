from rest_framework.throttling import UserRateThrottle

from src.core.settings import THROTTLE_10_PER_MINUTE, THROTTLE_25_PER_HOUR


class ListBrandsRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class CreateBrandRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_25_PER_HOUR


class UpdateBrandRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_25_PER_HOUR


class DeleteBrandRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_25_PER_HOUR


class ListCategoriesRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class CreateCategoryRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_25_PER_HOUR


class UpdateCategoryRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_25_PER_HOUR


class DeleteCategoryRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_25_PER_HOUR


class ListProductsRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class CreateProductRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_25_PER_HOUR


class GetProductRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_10_PER_MINUTE


class UpdateProductRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_25_PER_HOUR


class DeleteProductRateThrottle(UserRateThrottle):
    rate: str = THROTTLE_25_PER_HOUR
