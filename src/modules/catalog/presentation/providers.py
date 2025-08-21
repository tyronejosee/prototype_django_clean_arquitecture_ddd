from functools import lru_cache

from src.modules.catalog.application.use_cases.create_brand import CreateBrandUseCase
from src.modules.catalog.application.use_cases.create_category import CreateCategoryUseCase
from src.modules.catalog.application.use_cases.create_product import CreateProductUseCase
from src.modules.catalog.application.use_cases.delete_brand import DeleteBrandUseCase
from src.modules.catalog.application.use_cases.delete_category import DeleteCategoryUseCase
from src.modules.catalog.application.use_cases.delete_product import DeleteProductUseCase
from src.modules.catalog.application.use_cases.get_brand import GetBrandUseCase
from src.modules.catalog.application.use_cases.get_category import GetCategoryUseCase
from src.modules.catalog.application.use_cases.get_product import GetProductUseCase
from src.modules.catalog.application.use_cases.list_brands import ListBrandsUseCase
from src.modules.catalog.application.use_cases.list_categories import ListCategoriesUseCase
from src.modules.catalog.application.use_cases.list_featured_products import ListFeaturedProductsUseCase
from src.modules.catalog.application.use_cases.list_products import ListProductsUseCase
from src.modules.catalog.application.use_cases.list_products_by_brand import ListProductsByBrandUseCase
from src.modules.catalog.application.use_cases.list_products_by_category import ListProductsByCategoryUseCase
from src.modules.catalog.application.use_cases.update_brand import UpdateBrandUseCase
from src.modules.catalog.application.use_cases.update_category import UpdateCategoryUseCase
from src.modules.catalog.application.use_cases.update_product import UpdateProductUseCase
from src.modules.catalog.infrastructure.cache.brand_cache_service import BrandCacheService
from src.modules.catalog.infrastructure.cache.category_cache_service import CategoryCacheService
from src.modules.catalog.infrastructure.cache.product_cache_service import ProductCacheService
from src.modules.catalog.infrastructure.repositories.brand_repository import BrandRepository
from src.modules.catalog.infrastructure.repositories.category_repository import CategoryRepository
from src.modules.catalog.infrastructure.repositories.product_repository import ProductRepository


@lru_cache
def get_category_repository() -> CategoryRepository:
    return CategoryRepository()


@lru_cache
def get_category_cache() -> CategoryCacheService:
    return CategoryCacheService()


@lru_cache
def get_brand_repository() -> BrandRepository:
    return BrandRepository()


@lru_cache
def get_brand_cache() -> BrandCacheService:
    return BrandCacheService()


@lru_cache
def get_product_repository() -> ProductRepository:
    return ProductRepository()


@lru_cache
def get_product_cache() -> ProductCacheService:
    return ProductCacheService()


def get_list_brands_use_case() -> ListBrandsUseCase:
    return ListBrandsUseCase(repo=get_brand_repository(), cache=get_brand_cache())


def get_create_brand_use_case() -> CreateBrandUseCase:
    return CreateBrandUseCase(repo=get_brand_repository(), cache=get_brand_cache())


def get_get_brand_use_case() -> GetBrandUseCase:
    return GetBrandUseCase(repo=get_brand_repository())


def get_update_brand_use_case() -> UpdateBrandUseCase:
    return UpdateBrandUseCase(repo=get_brand_repository(), cache=get_brand_cache())


def get_delete_brand_use_case() -> DeleteBrandUseCase:
    return DeleteBrandUseCase(repo=get_brand_repository(), cache=get_brand_cache())


def get_list_categories_use_case() -> ListCategoriesUseCase:
    return ListCategoriesUseCase(repo=get_category_repository(), cache=get_category_cache())


def get_create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase(repo=get_category_repository(), cache=get_category_cache())


def get_get_category_use_case() -> GetCategoryUseCase:
    return GetCategoryUseCase(repo=get_category_repository())


def get_update_category_use_case() -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase(repo=get_category_repository(), cache=get_category_cache())


def get_delete_category_use_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase(repo=get_category_repository(), cache=get_category_cache())


def get_list_products_use_case() -> ListProductsUseCase:
    return ListProductsUseCase(repo=get_product_repository(), cache=get_product_cache())


def get_create_product_use_case() -> CreateProductUseCase:
    return CreateProductUseCase(repo=get_product_repository(), cache=get_product_cache())


def get_get_product_use_case() -> GetProductUseCase:
    return GetProductUseCase(repo=get_product_repository())


def get_update_product_use_case() -> UpdateProductUseCase:
    return UpdateProductUseCase(repo=get_product_repository(), cache=get_product_cache())


def get_delete_product_use_case() -> DeleteProductUseCase:
    return DeleteProductUseCase(repo=get_product_repository(), cache=get_product_cache())


def get_list_featured_products_use_case() -> ListFeaturedProductsUseCase:
    return ListFeaturedProductsUseCase(repo=get_product_repository(), cache=get_product_cache())


def get_list_products_by_category_use_case() -> ListProductsByCategoryUseCase:
    return ListProductsByCategoryUseCase(
        product_repo=get_product_repository(), category_repo=get_category_repository(), cache=get_product_cache()
    )


def get_list_products_by_brand_use_case() -> ListProductsByBrandUseCase:
    return ListProductsByBrandUseCase(
        product_repo=get_product_repository(), brand_repo=get_brand_repository(), cache=get_product_cache()
    )
