from decimal import Decimal
from unittest.mock import Mock, ANY, patch
from uuid import uuid4

import pytest

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
from src.modules.catalog.domain.entities.brand import Brand
from src.modules.catalog.domain.entities.category import Category
from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.exceptions import (
    BrandDomainError,
    BrandNotFoundError,
    CategoryDomainError,
    CategoryNotFoundError,
    ProductDomainError,
)
from src.modules.catalog.domain.factories.brand_factory import BrandFactory
from src.modules.catalog.domain.factories.category_factory import CategoryFactory
from src.modules.catalog.domain.factories.product_factory import ProductFactory
from src.modules.catalog.domain.interfaces.brand_cache_interface import BrandCacheInterface
from src.modules.catalog.domain.interfaces.brand_repository_interface import BrandRepositoryInterface
from src.modules.catalog.domain.interfaces.category_cache_interface import CategoryCacheInterface
from src.modules.catalog.domain.interfaces.category_repository_interface import CategoryRepositoryInterface
from src.modules.catalog.domain.interfaces.product_cache_interface import ProductCacheInterface
from src.modules.catalog.domain.interfaces.product_repository_interface import ProductRepositoryInterface
from src.modules.catalog.domain.utils.brand_cache_keys import BrandCacheKeys
from src.modules.catalog.domain.utils.category_cache_keys import CategoryCacheKeys
from src.modules.catalog.domain.utils.product_cache_keys import ProductCacheKeys


class TestCreateBrandUseCase:
    def test_create_brand_successfully(self) -> None:
        # Given: repo mock, cache mock, and brand data
        repo_mock = Mock()
        cache_mock = Mock()
        brand_data = {"name": "Nike"}
        expected_brand = BrandFactory.from_dict(brand_data)
        repo_mock.exists_by_name.return_value = False
        repo_mock.create.return_value = expected_brand

        # When: executing the use case with the brand data
        use_case = CreateBrandUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute(brand_data)

        # Then: the result is a Brand with correct values
        assert isinstance(result, Brand)
        assert result.name.value == "Nike"
        assert result.slug.value == "nike"
        assert result.is_active is True
        repo_mock.exists_by_name.assert_called_once_with("Nike")
        repo_mock.create.assert_called_once_with(ANY)
        cache_mock.delete.assert_called_once_with(BrandCacheKeys.brand_list_key())

    def test_create_brand_raises_if_name_exists(self) -> None:
        # Given: repo mock configured to indicate brand name already exists
        repo_mock = Mock()
        cache_mock = Mock()
        brand_data = {"name": "Adidas"}
        repo_mock.exists_by_name.return_value = True

        # When/Then: executing the use case raises BrandDomainError
        use_case = CreateBrandUseCase(repo=repo_mock, cache=cache_mock)
        with pytest.raises(BrandDomainError) as exc_info:
            use_case.execute(brand_data)

        assert str(exc_info.value) == CreateBrandUseCase.BRAND_WITH_THAT_NAME_ALREADY_EXISTS_MSG
        repo_mock.exists_by_name.assert_called_once_with("Adidas")
        repo_mock.create.assert_not_called()
        cache_mock.delete.assert_not_called()


class TestCreateCategoryUseCase:
    def test_create_category_successfully(self) -> None:
        # Given: repo mock, cache mock, and category data
        repo_mock = Mock()
        cache_mock = Mock()
        category_data = {"name": "Electronics"}
        expected_category = CategoryFactory.from_dict(category_data)
        repo_mock.exists_by_name.return_value = False
        repo_mock.create.return_value = expected_category

        # When: executing the use case with the category data
        use_case = CreateCategoryUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute(category_data)

        # Then: the result is a Category with correct values
        assert isinstance(result, Category)
        assert result.name.value == "Electronics"
        assert result.slug.value == "electronics"
        assert result.is_active is True

        repo_mock.exists_by_name.assert_called_once_with("Electronics")
        repo_mock.create.assert_called_once_with(ANY)
        cache_mock.delete.assert_called_once_with(CategoryCacheKeys.category_list_key())

    def test_create_category_raises_if_name_exists(self) -> None:
        # Given: repo mock configured to indicate category name already exists
        repo_mock = Mock()
        cache_mock = Mock()
        category_data = {"name": "Home Appliances"}
        repo_mock.exists_by_name.return_value = True

        # When/Then: executing the use case raises CategoryDomainError
        use_case = CreateCategoryUseCase(repo=repo_mock, cache=cache_mock)
        with pytest.raises(CategoryDomainError) as exc_info:
            use_case.execute(category_data)

        assert str(exc_info.value) == CreateCategoryUseCase.CATEGORY_WITH_THAT_NAME_ALREADY_EXISTS_MSG
        repo_mock.exists_by_name.assert_called_once_with("Home Appliances")
        repo_mock.create.assert_not_called()
        cache_mock.delete.assert_not_called()


class TestCreateProductUseCase:
    def test_create_product_successfully(self) -> None:
        # Given: repo mock, cache mock, product data and image
        repo_mock = Mock()
        cache_mock = Mock()
        product_data = {
            "name": "Laptop",
            "description": "High-end gaming laptop",
            "sku": "LAP-1234",
            "price": "1200.00",
            "brand_id": uuid4(),
            "category_id": uuid4(),
        }
        image_bytes = b"fake image"
        expected_product = ProductFactory.from_dict(product_data)
        repo_mock.exists_by_sku.return_value = False
        repo_mock.create.return_value = expected_product

        # When: executing the use case with the product data
        use_case = CreateProductUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute(data=product_data, image=image_bytes)

        # Then: the result is a Product with correct values
        assert isinstance(result, Product)
        assert result.name == "Laptop"
        assert result.sku.value == "LAP-1234"
        assert result.price == Decimal("1200.00")
        assert result.category_id == product_data["category_id"]

        repo_mock.exists_by_sku.assert_called_once_with("LAP-1234")
        repo_mock.create.assert_called_once_with(product=ANY, image=image_bytes)
        cache_mock.delete.assert_any_call(ProductCacheKeys.product_list_key())
        cache_mock.delete.assert_any_call(ProductCacheKeys.product_list_featured_key())
        cache_mock.delete.assert_any_call(ProductCacheKeys.product_list_by_category_key(product_data["category_id"]))

    def test_create_product_raises_if_sku_exists(self) -> None:
        # Given: repo mock configured to indicate SKU already exists
        repo_mock = Mock()
        cache_mock = Mock()
        product_data = {
            "name": "Laptop",
            "sku": "LAP-1234",
            "price": 1200.0,
            "category_id": uuid4(),
        }
        image_bytes = b"fake image"
        repo_mock.exists_by_sku.return_value = True

        # When & Then: executing the use case raises ProductDomainError
        use_case = CreateProductUseCase(repo=repo_mock, cache=cache_mock)
        with pytest.raises(ProductDomainError) as exc_info:
            use_case.execute(data=product_data, image=image_bytes)

        assert str(exc_info.value) == CreateProductUseCase.SKU_ALREADY_EXISTS_MSG
        repo_mock.exists_by_sku.assert_called_once_with("LAP-1234")
        repo_mock.create.assert_not_called()
        cache_mock.delete.assert_not_called()


class TestDeleteBrandUseCase:
    def test_delete_brand_successfully(self) -> None:
        # Given: repo mock, cache mock, and a brand_id
        repo_mock = Mock(spec=BrandRepositoryInterface)
        cache_mock = Mock(spec=BrandCacheInterface)
        brand_id = uuid4()

        # When: executing the use case
        use_case = DeleteBrandUseCase(repo=repo_mock, cache=cache_mock)
        use_case.execute(brand_id)

        # Then: repo.delete and cache.delete are called with correct arguments
        cache_mock.delete.assert_called_once_with(BrandCacheKeys.brand_list_key())
        repo_mock.delete.assert_called_once_with(brand_id)


class TestDeleteCategoryUseCase:
    def test_delete_category_successfully(self) -> None:
        # Given: repo mock, cache mock, and a category_id
        repo_mock = Mock(spec=CategoryRepositoryInterface)
        cache_mock = Mock(spec=CategoryCacheInterface)
        category_id = uuid4()

        # When: executing the use case
        use_case = DeleteCategoryUseCase(repo=repo_mock, cache=cache_mock)
        use_case.execute(category_id)

        # Then: repo.delete and cache.delete are called with correct arguments
        cache_mock.delete.assert_called_once_with(CategoryCacheKeys.category_list_key())
        repo_mock.delete.assert_called_once_with(category_id)


class TestDeleteProductUseCase:
    def test_delete_product_successfully(self) -> None:
        # Given: repo mock, cache mock, and a product_id
        repo_mock = Mock(spec=ProductRepositoryInterface)
        cache_mock = Mock(spec=ProductCacheInterface)
        product_id = uuid4()

        # When: executing the use case
        use_case = DeleteProductUseCase(repo=repo_mock, cache=cache_mock)
        use_case.execute(product_id)

        # Then: all relevant cache keys are deleted
        cache_mock.delete.assert_any_call(ProductCacheKeys.product_list_key())
        cache_mock.delete.assert_any_call(ProductCacheKeys.product_list_featured_key())
        cache_mock.delete.assert_any_call(ProductCacheKeys.product_list_by_category_key(product_id))

        # And: repo.delete is called with the correct product_id
        repo_mock.delete.assert_called_once_with(product_id)


class TestGetBrandUseCase:
    def test_get_brand_successfully(self) -> None:
        # Given: repo mock and a brand_id
        repo_mock = Mock(spec=BrandRepositoryInterface)
        brand_id = uuid4()
        expected_brand = Mock(spec=Brand)
        repo_mock.get_by_id.return_value = expected_brand

        # When: executing the use case
        use_case = GetBrandUseCase(repo=repo_mock)
        result = use_case.execute(brand_id)

        # Then: the returned brand matches expected
        assert result == expected_brand
        repo_mock.get_by_id.assert_called_once_with(brand_id)

    def test_get_brand_returns_none_if_not_found(self) -> None:
        # Given: repo mock returning None
        repo_mock = Mock(spec=BrandRepositoryInterface)
        brand_id = uuid4()
        repo_mock.get_by_id.return_value = None

        # When: executing the use case
        use_case = GetBrandUseCase(repo=repo_mock)
        result = use_case.execute(brand_id)

        # Then: the result is None
        assert result is None
        repo_mock.get_by_id.assert_called_once_with(brand_id)


class TestGetCategoryUseCase:
    def test_get_category_successfully(self) -> None:
        # Given: repo mock and a category_id
        repo_mock = Mock(spec=CategoryRepositoryInterface)
        category_id = uuid4()
        expected_category = Mock(spec=Category)
        repo_mock.get_by_id.return_value = expected_category

        # When: executing the use case
        use_case = GetCategoryUseCase(repo=repo_mock)
        result = use_case.execute(category_id)

        # Then: the returned category matches expected
        assert result == expected_category
        repo_mock.get_by_id.assert_called_once_with(category_id)

    def test_get_category_returns_none_if_not_found(self) -> None:
        # Given: repo mock returning None
        repo_mock = Mock(spec=CategoryRepositoryInterface)
        category_id = uuid4()
        repo_mock.get_by_id.return_value = None

        # When: executing the use case
        use_case = GetCategoryUseCase(repo=repo_mock)
        result = use_case.execute(category_id)

        # Then: the result is None
        assert result is None
        repo_mock.get_by_id.assert_called_once_with(category_id)


class TestGetProductUseCase:
    def test_get_product_successfully(self) -> None:
        # Given: repo mock and a product_id
        repo_mock = Mock(spec=ProductRepositoryInterface)
        product_id = uuid4()
        expected_product = Mock(spec=Product)
        repo_mock.get_by_id.return_value = expected_product

        # When: executing the use case
        use_case = GetProductUseCase(repo=repo_mock)
        result = use_case.execute(product_id)

        # Then: the returned product matches expected
        assert result == expected_product
        repo_mock.get_by_id.assert_called_once_with(product_id)

    def test_get_product_returns_none_if_not_found(self) -> None:
        # Given: repo mock returning None
        repo_mock = Mock(spec=ProductRepositoryInterface)
        product_id = uuid4()
        repo_mock.get_by_id.return_value = None

        # When: executing the use case
        use_case = GetProductUseCase(repo=repo_mock)
        result = use_case.execute(product_id)

        # Then: the result is None
        assert result is None
        repo_mock.get_by_id.assert_called_once_with(product_id)


class TestListBrandsUseCase:
    def test_list_brands_returns_from_cache(self) -> None:
        # Given: cache with data
        repo_mock = Mock()
        cache_mock = Mock()
        expected_brands = [Mock(spec=Brand)]
        cache_mock.get.return_value = expected_brands

        # When: executing the use case
        use_case = ListBrandsUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute()

        # Then: returns cached brands
        assert result == expected_brands
        cache_mock.get.assert_called_once_with(BrandCacheKeys.brand_list_key())
        repo_mock.list_all.assert_not_called()
        cache_mock.set.assert_not_called()

    def test_list_brands_fallbacks_to_repo_and_sets_cache(self) -> None:
        # Given: empty cache
        repo_mock = Mock()
        cache_mock = Mock()
        expected_brands = [Mock(spec=Brand)]
        cache_mock.get.return_value = None
        repo_mock.list_all.return_value = expected_brands

        # When: executing the use case
        use_case = ListBrandsUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute()

        # Then: returns repo result and sets cache
        assert result == expected_brands
        cache_mock.get.assert_called_once_with(BrandCacheKeys.brand_list_key())
        repo_mock.list_all.assert_called_once_with()
        cache_mock.set.assert_called_once_with(BrandCacheKeys.brand_list_key(), expected_brands)


class TestListCategoriesUseCase:
    def test_list_categories_returns_from_cache(self) -> None:
        # Given: cache with categories
        repo_mock = Mock()
        cache_mock = Mock()
        expected_categories = [Mock(spec=Category)]
        cache_mock.get.return_value = expected_categories

        # When: executing the use case
        use_case = ListCategoriesUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute()

        # Then: returns cached categories
        assert result == expected_categories
        cache_mock.get.assert_called_once_with(CategoryCacheKeys.category_list_key())
        repo_mock.list_all.assert_not_called()
        cache_mock.set.assert_not_called()

    def test_list_categories_fallbacks_to_repo_and_sets_cache(self) -> None:
        # Given: cache is empty
        repo_mock = Mock()
        cache_mock = Mock()
        expected_categories = [Mock(spec=Category)]
        cache_mock.get.return_value = None
        repo_mock.list_all.return_value = expected_categories

        # When: executing the use case
        use_case = ListCategoriesUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute()

        # Then: returns repo result and updates cache
        assert result == expected_categories
        cache_mock.get.assert_called_once_with(CategoryCacheKeys.category_list_key())
        repo_mock.list_all.assert_called_once_with()
        cache_mock.set.assert_called_once_with(CategoryCacheKeys.category_list_key(), expected_categories)


class TestListFeaturedProductsUseCase:
    def test_list_featured_products_returns_from_cache(self) -> None:
        # Given: cache has products
        repo_mock = Mock()
        cache_mock = Mock()
        expected_products = [Mock(spec=Product)]
        cache_mock.get.return_value = expected_products

        # When: executing the use case
        use_case = ListFeaturedProductsUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute(limit=5)

        # Then: returns cached products
        assert result == expected_products
        cache_mock.get.assert_called_once_with(ProductCacheKeys.product_list_featured_key())
        repo_mock.list_featured.assert_not_called()
        cache_mock.set.assert_not_called()

    def test_list_featured_products_fallbacks_to_repo_and_sets_cache(self) -> None:
        # Given: cache is empty
        repo_mock = Mock()
        cache_mock = Mock()
        repo_products = [Mock(spec=Product) for _ in range(20)]
        repo_mock.list_featured.return_value = repo_products
        cache_mock.get.return_value = None
        limit = 10
        expected_products = repo_products[:limit]

        # When: executing the use case
        use_case = ListFeaturedProductsUseCase(repo=repo_mock, cache=cache_mock)
        result = use_case.execute(limit=limit)

        # Then: returns limited repo products and updates cache
        assert result == expected_products
        cache_mock.get.assert_called_once_with(ProductCacheKeys.product_list_featured_key())
        repo_mock.list_featured.assert_called_once_with()
        cache_mock.set.assert_called_once_with(ProductCacheKeys.product_list_featured_key(), expected_products)


class TestListProductsByBrandUseCase:
    def test_returns_cached_products_if_available(self) -> None:
        # Given: cache contains products for the brand
        product_repo = Mock(spec=ProductRepositoryInterface)
        brand_repo = Mock(spec=BrandRepositoryInterface)
        cache = Mock(spec=ProductCacheInterface)

        brand_id = uuid4()
        cached_products = [Mock(spec=Product)]
        cache.get.return_value = cached_products

        use_case = ListProductsByBrandUseCase(product_repo, brand_repo, cache)

        # When: executing the use case
        result = use_case.execute(brand_id)

        # Then: products are returned from cache without hitting repos
        assert result == cached_products
        cache.get.assert_called_once_with(ProductCacheKeys.product_list_by_brand_key(brand_id))
        brand_repo.exists.assert_not_called()
        product_repo.list_by_brand.assert_not_called()
        cache.set.assert_not_called()

    def test_raises_if_brand_not_found(self) -> None:
        # Given: cache empty and brand does not exist
        product_repo = Mock(spec=ProductRepositoryInterface)
        brand_repo = Mock(spec=BrandRepositoryInterface)
        cache = Mock(spec=ProductCacheInterface)

        brand_id = uuid4()
        cache.get.return_value = None
        brand_repo.exists.return_value = False

        use_case = ListProductsByBrandUseCase(product_repo, brand_repo, cache)

        # When & Then: exception is raised
        with pytest.raises(BrandNotFoundError) as exc_info:
            use_case.execute(brand_id)

        assert str(exc_info.value) == ListProductsByBrandUseCase.BRAND_NOT_FOUND_MSG
        cache.get.assert_called_once_with(ProductCacheKeys.product_list_by_brand_key(brand_id))
        brand_repo.exists.assert_called_once_with(brand_id)
        product_repo.list_by_brand.assert_not_called()
        cache.set.assert_not_called()

    def test_fetches_and_caches_products_if_not_cached(self) -> None:
        # Given: cache empty, brand exists, and repo has products
        product_repo = Mock(spec=ProductRepositoryInterface)
        brand_repo = Mock(spec=BrandRepositoryInterface)
        cache = Mock(spec=ProductCacheInterface)

        brand_id = uuid4()
        cache.get.return_value = None
        brand_repo.exists.return_value = True
        expected_products = [Mock(spec=Product)]
        product_repo.list_by_brand.return_value = expected_products

        use_case = ListProductsByBrandUseCase(product_repo, brand_repo, cache)

        # When: executing the use case
        result = use_case.execute(brand_id)

        # Then: repo is called, products are cached, and returned
        assert result == expected_products
        cache.get.assert_called_once_with(ProductCacheKeys.product_list_by_brand_key(brand_id))
        brand_repo.exists.assert_called_once_with(brand_id)
        product_repo.list_by_brand.assert_called_once_with(brand_id)
        cache.set.assert_called_once_with(ProductCacheKeys.product_list_by_brand_key(brand_id), expected_products)


class TestListProductsByCategoryUseCase:
    def test_returns_cached_products_if_available(self) -> None:
        # Given: category_id and products in cache
        category_id = uuid4()
        product_repo = Mock(spec=ProductRepositoryInterface)
        category_repo = Mock(spec=CategoryRepositoryInterface)
        cache = Mock(spec=ProductCacheInterface)

        cached_products = [Mock(spec=Product)]
        cache.get.return_value = cached_products

        use_case = ListProductsByCategoryUseCase(product_repo, category_repo, cache)

        # When: executing the use case
        result = use_case.execute(category_id)

        # Then: products come from cache
        assert result == cached_products
        cache.get.assert_called_once_with(ProductCacheKeys.product_list_by_category_key(category_id))
        product_repo.list_by_category.assert_not_called()
        cache.set.assert_not_called()

    def test_raises_error_if_category_not_found(self) -> None:
        # Given: category does not exist
        category_id = uuid4()
        product_repo = Mock(spec=ProductRepositoryInterface)
        category_repo = Mock(spec=CategoryRepositoryInterface)
        cache = Mock(spec=ProductCacheInterface)

        cache.get.return_value = None
        category_repo.exists.return_value = False

        use_case = ListProductsByCategoryUseCase(product_repo, category_repo, cache)

        # When & Then: raises CategoryNotFoundError
        with pytest.raises(CategoryNotFoundError, match="Category not found."):
            use_case.execute(category_id)

        cache.get.assert_called_once()
        category_repo.exists.assert_called_once_with(category_id)
        product_repo.list_by_category.assert_not_called()
        cache.set.assert_not_called()

    def test_fetches_and_caches_products_if_not_cached(self) -> None:
        # Given: cache empty, category exists, repo returns products
        category_id = uuid4()
        product_repo = Mock(spec=ProductRepositoryInterface)
        category_repo = Mock(spec=CategoryRepositoryInterface)
        cache = Mock(spec=ProductCacheInterface)

        cache.get.return_value = None
        category_repo.exists.return_value = True
        expected_products = [Mock(spec=Product)]
        product_repo.list_by_category.return_value = expected_products

        use_case = ListProductsByCategoryUseCase(product_repo, category_repo, cache)

        # When: executing the use case
        result = use_case.execute(category_id)

        # Then: repo is called, products cached and returned
        assert result == expected_products
        cache.get.assert_called_once_with(ProductCacheKeys.product_list_by_category_key(category_id))
        category_repo.exists.assert_called_once_with(category_id)
        product_repo.list_by_category.assert_called_once_with(category_id)
        cache.set.assert_called_once_with(ProductCacheKeys.product_list_by_category_key(category_id), expected_products)


class TestListProductsUseCase:
    def test_returns_cached_products_if_available(self) -> None:
        # Given: cache contains products
        repo = Mock(spec=ProductRepositoryInterface)
        cache = Mock(spec=ProductCacheInterface)

        cached_products = [Mock(spec=Product)]
        cache.get.return_value = cached_products

        use_case = ListProductsUseCase(repo, cache)
        query_params = {"limit": 10}

        # When: executing the use case
        result = use_case.execute(query_params)

        # Then: products are returned from cache
        assert result == cached_products
        cache.get.assert_called_once_with(ProductCacheKeys.product_list_key())
        repo.list_all.assert_not_called()
        cache.set.assert_not_called()

    def test_fetches_and_caches_products_if_not_cached(self) -> None:
        # Given: cache empty and repo returns products
        repo = Mock(spec=ProductRepositoryInterface)
        cache = Mock(spec=ProductCacheInterface)

        cache.get.return_value = None
        expected_products = [Mock(spec=Product)]
        repo.list_all.return_value = expected_products

        use_case = ListProductsUseCase(repo, cache)
        query_params = {"limit": 5, "offset": 0}

        # When: executing the use case
        result = use_case.execute(query_params)

        # Then: repo is called, result cached, and returned
        assert result == expected_products
        cache.get.assert_called_once_with(ProductCacheKeys.product_list_key())
        repo.list_all.assert_called_once_with(query_params)
        cache.set.assert_called_once_with(ProductCacheKeys.product_list_key(), expected_products)


class TestUpdateBrandUseCase:
    def test_updates_brand_and_clears_cache(self) -> None:
        # Given: repo and cache mocks
        brand_id = uuid4()
        data = {"name": "New Brand"}
        repo = Mock(spec=BrandRepositoryInterface)
        cache = Mock(spec=BrandCacheInterface)

        updated_brand = Mock(spec=Brand)
        repo.update.return_value = updated_brand

        use_case = UpdateBrandUseCase(repo, cache)

        # Patch BrandFactory to control from_dict
        with patch.object(BrandFactory, "from_dict", return_value=Mock(spec=Brand)) as mock_factory:
            # When: executing the use case
            result = use_case.execute(brand_id, data)

        # Then: repo and cache used correctly
        assert result == updated_brand
        mock_factory.assert_called_once_with(data)
        repo.update.assert_called_once_with(brand_id=brand_id, brand=mock_factory.return_value)
        cache.delete.assert_called_once_with(BrandCacheKeys.brand_list_key())

    def test_returns_updated_brand(self) -> None:
        # Given: setup mocks
        brand_id = uuid4()
        data = {"name": "Updated Brand"}
        repo = Mock(spec=BrandRepositoryInterface)
        cache = Mock(spec=BrandCacheInterface)

        expected_brand = Mock(spec=Brand)
        repo.update.return_value = expected_brand

        use_case = UpdateBrandUseCase(repo, cache)

        with patch.object(BrandFactory, "from_dict", return_value=Mock(spec=Brand)):
            # When: executing
            result = use_case.execute(brand_id, data)

        # Then: returns the brand from repo.update
        assert result == expected_brand


class TestUpdateCategoryUseCase:
    def test_updates_category_and_clears_cache(self) -> None:
        # Given: repo and cache mocks
        category_id = uuid4()
        data = {"name": "New Category"}
        repo = Mock(spec=CategoryRepositoryInterface)
        cache = Mock(spec=CategoryCacheInterface)

        updated_category = Mock(spec=Category)
        repo.update.return_value = updated_category

        use_case = UpdateCategoryUseCase(repo, cache)

        # Patch CategoryFactory to control from_dict
        with patch.object(CategoryFactory, "from_dict", return_value=Mock(spec=Category)) as mock_factory:
            # When: executing the use case
            result = use_case.execute(category_id, data)

        # Then: repo.update and cache.delete called correctly
        assert result == updated_category
        mock_factory.assert_called_once_with(data)
        repo.update.assert_called_once_with(category_id=category_id, category=mock_factory.return_value)
        cache.delete.assert_called_once_with(CategoryCacheKeys.category_list_key())

    def test_returns_updated_category(self) -> None:
        # Given: setup mocks
        category_id = uuid4()
        data = {"name": "Updated Category"}
        repo = Mock(spec=CategoryRepositoryInterface)
        cache = Mock(spec=CategoryCacheInterface)

        expected_category = Mock(spec=Category)
        repo.update.return_value = expected_category

        use_case = UpdateCategoryUseCase(repo, cache)

        with patch.object(CategoryFactory, "from_dict", return_value=Mock(spec=Category)):
            # When: executing
            result = use_case.execute(category_id, data)

        # Then: returns the category from repo.update
        assert result == expected_category


class TestUpdateProductUseCase:
    def test_updates_product_and_clears_cache(self) -> None:
        # Given: repo and cache mocks
        product_id = uuid4()
        category_id = uuid4()
        data = {"name": "New Product", "category_id": category_id}
        image = b"fake-image-bytes"

        repo = Mock(spec=ProductRepositoryInterface)
        cache = Mock(spec=ProductCacheInterface)

        updated_product = Mock(spec=Product)
        updated_product.category_id = category_id
        repo.update.return_value = updated_product

        use_case = UpdateProductUseCase(repo, cache)

        # Patch ProductFactory.from_dict to control creation
        with patch.object(ProductFactory, "from_dict", return_value=Mock(spec=Product)) as mock_factory:
            # When: executing the use case
            result = use_case.execute(product_id, data, image=image)

        # Then: repo.update and cache.delete called correctly
        assert result == updated_product
        mock_factory.assert_called_once_with(data)
        repo.update.assert_called_once_with(product=mock_factory.return_value, product_id=product_id, image=image)

        expected_keys = (
            ProductCacheKeys.product_list_key(),
            ProductCacheKeys.product_list_featured_key(),
            ProductCacheKeys.product_list_by_category_key(category_id),
        )
        for key in expected_keys:
            cache.delete.assert_any_call(key)

    def test_returns_updated_product(self) -> None:
        # Given: repo returns a product
        product_id = uuid4()
        category_id = uuid4()
        data = {"name": "Updated Product", "category_id": category_id}
        repo = Mock(spec=ProductRepositoryInterface)
        cache = Mock(spec=ProductCacheInterface)

        expected_product = Mock(spec=Product)
        expected_product.category_id = category_id
        repo.update.return_value = expected_product

        use_case = UpdateProductUseCase(repo, cache)

        with patch.object(ProductFactory, "from_dict", return_value=Mock(spec=Product)):
            # When: executing
            result = use_case.execute(product_id, data)

        # Then: returns the product from repo.update
        assert result == expected_product
