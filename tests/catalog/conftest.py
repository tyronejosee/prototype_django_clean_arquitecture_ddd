import pytest

from src.modules.catalog.infrastructure.models.brand_model import BrandModel
from src.modules.catalog.infrastructure.models.category_model import CategoryModel
from src.modules.catalog.infrastructure.models.product_model import ProductModel
from tests.catalog.factories import BrandModelFactory, CategoryModelFactory, ProductModelFactory


@pytest.fixture
def brand() -> BrandModel:
    return BrandModelFactory()


@pytest.fixture
def category() -> CategoryModel:
    return CategoryModelFactory()


@pytest.fixture
def product(brand: BrandModel, category: CategoryModel) -> ProductModel:
    return ProductModelFactory()
