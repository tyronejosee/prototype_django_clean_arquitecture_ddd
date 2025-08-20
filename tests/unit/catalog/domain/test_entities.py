from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.modules.catalog.domain.entities.brand import Brand
from src.modules.catalog.domain.entities.category import Category
from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.exceptions import (
    BrandDomainError,
    CatalogDomainError,
    CategoryDomainError,
    ProductDomainError,
)
from src.modules.catalog.domain.value_objects.brand_name import BrandName
from src.modules.catalog.domain.value_objects.category_name import CategoryName
from src.modules.catalog.domain.value_objects.currency import Currency
from src.modules.catalog.domain.value_objects.sku import SKU
from src.modules.catalog.domain.value_objects.slug import Slug
from src.modules.catalog.domain.value_objects.weight_unit import WeightUnit


def build_valid_brand(**overrides) -> Brand:
    return Brand(
        id=overrides.get("id", uuid4()),
        name=overrides.get("name", BrandName("Nike")),
        slug=overrides.get("slug", Slug("nike")),
        is_active=overrides.get("is_active", True),
        created_at=overrides.get("created_at", datetime.now(UTC)),
        updated_at=overrides.get("updated_at", datetime.now(UTC)),
    )


class TestBrand:
    def test_valid_brand_passes_validation(self) -> None:
        # Given: a valid brand
        brand = build_valid_brand()

        # Then: attributes should be correctly set
        assert brand.name.value == "Nike"
        assert brand.slug.value == "nike"
        assert brand.is_active is True

    def test_brand_can_be_inactive(self) -> None:
        # Given: a brand explicitly set as inactive
        brand = build_valid_brand(is_active=False)

        # Then: the brand should reflect that state
        assert brand.is_active is False

    def test_brand_created_at_and_updated_at_are_optional(self) -> None:
        # Given: a brand without explicit timestamps
        brand = Brand(id=uuid4(), name=BrandName("Adidas"), slug=Slug("adidas"))

        # When & Then: created_at and updated_at should be None
        assert brand.created_at is None
        assert brand.updated_at is None

    def test_brand_name_must_not_be_blank(self) -> None:
        # Given: an invalid blank brand name
        # When & Then: an error should be raised
        with pytest.raises(BrandDomainError):
            build_valid_brand(name=BrandName(" "))

    def test_brand_slug_must_not_be_blank(self) -> None:
        # Given: an invalid blank slug
        # When & Then: an error should be raised
        with pytest.raises(CatalogDomainError):
            build_valid_brand(slug=Slug(" "))


def build_valid_category(**overrides) -> Category:
    return Category(
        id=overrides.get("id", uuid4()),
        name=overrides.get("name", CategoryName("Shoes")),
        slug=overrides.get("slug", Slug("shoes")),
        description=overrides.get("description", "Category for shoes"),
        is_active=overrides.get("is_active", True),
        created_at=overrides.get("created_at", datetime.now(UTC)),
        updated_at=overrides.get("updated_at", datetime.now(UTC)),
    )


class TestCategory:
    def test_valid_category_passes_validation(self) -> None:
        # Given: a valid category
        category = build_valid_category()

        # When & Then: attributes should be correctly assigned
        assert category.name.value == "Shoes"
        assert category.slug.value == "shoes"
        assert category.description == "Category for shoes"
        assert category.is_active is True

    def test_category_can_be_inactive(self) -> None:
        # Given: a category explicitly set as inactive
        category = build_valid_category(is_active=False)

        # When & Then: the category should reflect that state
        assert category.is_active is False

    def test_category_description_defaults_to_empty_string(self) -> None:
        # Given: a category without description
        category = Category(id=uuid4(), name=CategoryName("Clothing"), slug=Slug("clothing"))

        # When & Then: description should be empty string
        assert category.description == ""

    def test_category_created_at_and_updated_at_are_optional(self) -> None:
        # Given: a category without timestamps
        category = Category(id=uuid4(), name=CategoryName("Accessories"), slug=Slug("accessories"))

        # When & Then: created_at and updated_at should be None
        assert category.created_at is None
        assert category.updated_at is None

    def test_category_name_must_not_be_blank(self) -> None:
        # Given: an invalid blank category name
        # When & Then: an error should be raised
        with pytest.raises(CategoryDomainError):
            build_valid_category(name=CategoryName(" "))

    def test_category_slug_must_not_be_blank(self) -> None:
        # Given: an invalid blank slug
        # When & Then: an error should be raised
        with pytest.raises(CatalogDomainError):
            build_valid_category(slug=Slug(" "))


def build_valid_product(**overrides) -> Product:
    return Product(
        id=overrides.get("id", uuid4()),
        name=overrides.get("name", "Protein Bar"),
        slug=overrides.get("slug", Slug("protein-bar")),
        description=overrides.get("description", "High protein snack."),
        sku=overrides.get("sku", SKU("SKU123")),
        category_id=overrides.get("category_id", uuid4()),
        brand_id=overrides.get("brand_id", uuid4()),
        price=overrides.get("price", Decimal("10.00")),
        discount_price=overrides.get("discount_price", Decimal("8.00")),
        currency=overrides.get("currency", Currency("USD")),
        stock=overrides.get("stock", 10),
        min_stock=overrides.get("min_stock", 5),
        warehouse_location=overrides.get("warehouse_location", "A1"),
        image_url=overrides.get("image_url", "http://example.com/image.png"),
        is_active=overrides.get("is_active", True),
        is_featured=overrides.get("is_featured", False),
        weight=overrides.get("weight", Decimal("0.5")),
        unit=overrides.get("unit", WeightUnit("kg")),
        nutritional_info=overrides.get("nutritional_info", {"calories": 200}),
        ingredients=overrides.get("ingredients", {"main": "whey protein"}),
        allergens=overrides.get("allergens", {"milk": True}),
        created_at=overrides.get("created_at", datetime.now(UTC)),
        updated_at=overrides.get("updated_at", datetime.now(UTC)),
    )


class TestProduct:
    def test_valid_product_passes_validation(self) -> None:
        # Given: a valid product with default values
        product = build_valid_product()

        # When & Then: attributes should be correctly assigned
        assert product.name == "Protein Bar"
        assert product.price == Decimal("10.00")
        assert product.discount_price == Decimal("8.00")
        assert product.stock == 10
        assert product.is_active is True

    def test_product_name_required_raises_error(self) -> None:
        # Given: a product with no name
        # When & Then: an error should be raised
        with pytest.raises(ProductDomainError) as exc_info:
            build_valid_product(name="")
        assert "Name is required." in str(exc_info.value)

    def test_negative_price_raises_error(self) -> None:
        # Given: a product with a negative price
        # When & Then: an error should be raised
        with pytest.raises(ProductDomainError) as exc_info:
            build_valid_product(price=Decimal("-1.00"))
        assert "Price cannot be negative." in str(exc_info.value)

    def test_negative_discount_price_raises_error(self) -> None:
        # Given: a product with a negative discount price
        # When & Then: an error should be raised
        with pytest.raises(ProductDomainError) as exc_info:
            build_valid_product(discount_price=Decimal("-1.00"))
        assert "Discount price cannot be negative." in str(exc_info.value)

    def test_discount_price_higher_than_price_raises_error(self) -> None:
        # Given: a product with a discount price higher than its price
        # When & Then: an error should be raised
        with pytest.raises(ProductDomainError) as exc_info:
            build_valid_product(price=Decimal("10.00"), discount_price=Decimal("15.00"))
        assert "Discount price cannot exceed price." in str(exc_info.value)

    def test_negative_stock_raises_error(self) -> None:
        # Given: a product with a negative stock
        # When & Then: an error should be raised
        with pytest.raises(ProductDomainError) as exc_info:
            build_valid_product(stock=-5)
        assert "Stock cannot be negative." in str(exc_info.value)

    def test_stock_exceeds_maximum_raises_error(self) -> None:
        # Given: a product with a stock exceeding the maximum
        # When & Then: an error should be raised
        with pytest.raises(ProductDomainError) as exc_info:
            build_valid_product(stock=200)
        assert "Stock cannot exceed 100 units." in str(exc_info.value)

    def test_negative_min_stock_raises_error(self) -> None:
        # Given: a product with a negative minimum stock
        # When & Then: an error should be raised
        with pytest.raises(ProductDomainError) as exc_info:
            build_valid_product(min_stock=-1)
        assert "Min stock cannot be negative." in str(exc_info.value)

    def test_product_can_have_no_discount(self) -> None:
        # Given: a product with no discount price
        product = build_valid_product(discount_price=None)

        # When & Then: product should be valid
        assert product.discount_price is None
        assert product.price == Decimal("10.00")
