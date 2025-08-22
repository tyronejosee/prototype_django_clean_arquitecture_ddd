from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from src.modules.catalog.domain.entities.brand import Brand
from src.modules.catalog.domain.entities.category import Category
from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.factories.brand_factory import BrandFactory
from src.modules.catalog.domain.factories.category_factory import CategoryFactory
from src.modules.catalog.domain.factories.product_factory import ProductFactory
from src.modules.catalog.domain.value_objects.brand_name import BrandName
from src.modules.catalog.domain.value_objects.category_name import CategoryName
from src.modules.catalog.domain.value_objects.currency import Currency
from src.modules.catalog.domain.value_objects.sku import SKU
from src.modules.catalog.domain.value_objects.slug import Slug
from src.modules.catalog.domain.value_objects.weight_unit import WeightUnit


class TestBrandFactory:
    def test_brand_factory_from_dict_creates_valid_entity(self) -> None:
        # Given: a valid dictionary with brand data
        brand_id = uuid4()
        created = datetime.now(UTC) - timedelta(days=1)
        updated = datetime.now(UTC)

        data = {
            "id": brand_id,
            "name": "Nike",
            "is_active": True,
            "created_at": created,
            "updated_at": updated,
        }

        # When: creating a Brand from dict
        brand = BrandFactory.from_dict(data)

        # Then: the result should be a valid Brand object
        assert isinstance(brand, Brand)
        assert brand.id == brand_id
        assert brand.name == BrandName("Nike")
        assert brand.slug == Slug.from_name("Nike")
        assert brand.is_active is True
        assert brand.created_at == created
        assert brand.updated_at == updated

    def test_brand_factory_assigns_defaults_when_missing_fields(self) -> None:
        # Given: a minimal dict with only the required field
        data = {"name": "Adidas"}

        # When: creating the Brand
        brand = BrandFactory.from_dict(data)

        # Then: defaults should be assigned
        assert isinstance(brand, Brand)
        assert brand.name == BrandName("Adidas")
        assert brand.slug == Slug.from_name("Adidas")
        assert brand.is_active is True
        assert isinstance(brand.created_at, datetime)
        assert isinstance(brand.updated_at, datetime)
        assert brand.created_at.tzinfo == UTC
        assert brand.updated_at.tzinfo == UTC


class TestCategoryFactory:
    def test_category_factory_from_dict_creates_valid_entity(self) -> None:
        # Given: a valid dictionary with category data
        category_id = uuid4()
        created = datetime.now(UTC) - timedelta(days=2)
        updated = datetime.now(UTC)

        data = {
            "id": category_id,
            "name": "Electronics",
            "description": "All electronic products",
            "is_active": True,
            "created_at": created,
            "updated_at": updated,
        }

        # When: creating a Category from dict
        category = CategoryFactory.from_dict(data)

        # Then: the result should be a valid Category object
        assert isinstance(category, Category)
        assert category.id == category_id
        assert category.name == CategoryName("Electronics")
        assert category.slug == Slug.from_name("Electronics")
        assert category.description == "All electronic products"
        assert category.is_active is True
        assert category.created_at == created
        assert category.updated_at == updated

    def test_category_factory_assigns_defaults_when_missing_fields(self) -> None:
        # Given: minimal dict with only the required field
        data = {"name": "Books"}

        # When: creating the Category
        category = CategoryFactory.from_dict(data)

        # Then: defaults should be assigned
        assert isinstance(category, Category)
        assert category.name == CategoryName("Books")
        assert category.slug == Slug.from_name("Books")
        assert category.description == ""
        assert category.is_active is True
        assert isinstance(category.created_at, datetime)
        assert isinstance(category.updated_at, datetime)
        assert category.created_at.tzinfo == UTC
        assert category.updated_at.tzinfo == UTC


class TestProductFactory:
    def test_product_factory_from_dict_creates_valid_entity(self) -> None:
        # Given: a valid dictionary with product data
        product_id = uuid4()
        category_id = uuid4()
        brand_id = uuid4()
        created = datetime.now(UTC) - timedelta(days=1)
        updated = datetime.now(UTC)

        data = {
            "id": product_id,
            "name": "Laptop",
            "description": "High-end gaming laptop",
            "sku": "LAP123",
            "category_id": category_id,
            "brand_id": brand_id,
            "price": "1500.50",
            "discount_price": "1400.00",
            "currency": "USD",
            "stock": 10,
            "min_stock": 2,
            "warehouse_location": "A1",
            "image_url": "http://image.url/laptop.png",
            "is_active": True,
            "is_featured": True,
            "weight": "2.5",
            "unit": "kg",
            "nutritional_info": {},
            "ingredients": {},
            "allergens": {},
            "created_at": created,
            "updated_at": updated,
        }

        # When: creating a Product from dict
        product = ProductFactory.from_dict(data)

        # Then: the result should be a valid Product object
        assert isinstance(product, Product)
        assert product.id == product_id
        assert product.name == "Laptop"
        assert product.slug == Slug.from_name("Laptop")
        assert product.description == "High-end gaming laptop"
        assert product.sku == SKU("LAP123")
        assert product.category_id == category_id
        assert product.brand_id == brand_id
        assert product.price == Decimal("1500.50")
        assert product.discount_price == Decimal("1400.00")
        assert product.currency == Currency("USD")
        assert product.stock == 10
        assert product.min_stock == 2
        assert product.warehouse_location == "A1"
        assert product.image_url == "http://image.url/laptop.png"
        assert product.is_active is True
        assert product.is_featured is True
        assert product.weight == Decimal("2.5")
        assert product.unit == WeightUnit("kg")
        assert product.nutritional_info == {}
        assert product.ingredients == {}
        assert product.allergens == {}
        assert product.created_at == created
        assert product.updated_at == updated

    def test_product_factory_assigns_defaults_when_missing_fields(self) -> None:
        # Given: minimal dictionary with only required fields
        data = {
            "name": "Smartphone",
            "description": "Latest model",
            "sku": "SP123",
            "category_id": uuid4(),
            "brand_id": uuid4(),
            "price": "799.99",
            "weight": "0.5",
        }

        # When: creating the Product
        product = ProductFactory.from_dict(data)

        # Then: defaults should be assigned
        assert isinstance(product, Product)
        assert product.name == "Smartphone"
        assert product.slug == Slug.from_name("Smartphone")
        assert product.description == "Latest model"
        assert product.sku == SKU("SP123")
        assert product.price == Decimal("799.99")
        assert product.discount_price is None
        assert product.currency == Currency("USD")
        assert product.stock == 0
        assert product.min_stock == 5
        assert product.warehouse_location == ""
        assert product.image_url == ""
        assert product.is_active is True
        assert product.is_featured is False
        assert product.weight == Decimal("0.5")
        assert product.unit == WeightUnit("kg")
        assert product.nutritional_info == {}
        assert product.ingredients == {}
        assert product.allergens == {}
        assert isinstance(product.created_at, datetime)
        assert isinstance(product.updated_at, datetime)
        assert product.created_at.tzinfo == UTC
        assert product.updated_at.tzinfo == UTC
