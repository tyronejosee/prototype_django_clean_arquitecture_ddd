import pytest

from src.modules.catalog.domain.exceptions import (
    BrandDomainError,
    CatalogDomainError,
    CategoryDomainError,
    ProductDomainError,
)
from src.modules.catalog.domain.value_objects.brand_name import BrandName
from src.modules.catalog.domain.value_objects.category_name import CategoryName
from src.modules.catalog.domain.value_objects.currency import Currency
from src.modules.catalog.domain.value_objects.product_name import ProductName
from src.modules.catalog.domain.value_objects.sku import SKU
from src.modules.catalog.domain.value_objects.slug import Slug
from src.modules.catalog.domain.value_objects.weight_unit import WeightUnit


class TestBrandName:
    def test_valid_brand_name_creates_successfully(self) -> None:
        # Given: a valid brand name
        name = "MyBrand"

        # When: creating the BrandName
        result = BrandName(name)

        # Then: it should store the value
        assert result.value == name

    @pytest.mark.parametrize("name", ["", None])
    def test_brand_name_required_raises_error(self, name: str | None) -> None:
        # Given: an empty or missing brand name
        # When & Then: should raise a validation error
        with pytest.raises(BrandDomainError, match="required"):
            BrandName(name)  # type: ignore

    @pytest.mark.parametrize("name", ["forbidden", "BADWORD", "Test", "invalid"])
    def test_brand_name_forbidden_words_raises_error(self, name: str) -> None:
        # Given: a forbidden brand name
        # When & Then: should raise a domain error
        with pytest.raises(BrandDomainError, match="not allowed"):
            BrandName(name)


class TestCategoryName:
    def test_valid_category_name_creates_successfully(self) -> None:
        # Given: a valid category name
        name = "Electronics"

        # When: creating the CategoryName
        result = CategoryName(name)

        # Then: it should store the value
        assert result.value == name

    @pytest.mark.parametrize("name", ["", None])
    def test_category_name_required_raises_error(self, name: str | None) -> None:
        # Given: an empty or missing category name
        # When & Then: should raise a validation error
        with pytest.raises(CategoryDomainError, match="required"):
            CategoryName(name)  # type: ignore

    @pytest.mark.parametrize("name", ["forbidden", "BADWORD", "Test", "invalid"])
    def test_category_name_forbidden_words_raises_error(self, name: str) -> None:
        # Given: a forbidden category name
        # When & Then: should raise a domain error
        with pytest.raises(CategoryDomainError, match="not allowed"):
            CategoryName(name)


class TestCurrency:
    @pytest.mark.parametrize("value", ["USD", "CLP"])
    def test_valid_currency_creates_successfully(self, value: str) -> None:
        # Given: a valid currency code
        # When: creating the Currency
        result = Currency(value)

        # Then: it should store the value
        assert result.value == value

    @pytest.mark.parametrize("value", ["EUR", "BTC", "", None])
    def test_invalid_currency_raises_error(self, value: str | None) -> None:
        # Given: an invalid currency code
        # When & Then: should raise a domain error
        with pytest.raises(ProductDomainError, match="Invalid currency"):
            Currency(value)  # type: ignore


class TestProductName:
    def test_valid_product_name_creates_successfully(self) -> None:
        # Given: a valid product name
        name = "Laptop"

        # When: creating the ProductName
        result = ProductName(name)

        # Then: it should store the value
        assert result.value == name

    @pytest.mark.parametrize("name", ["", None])
    def test_product_name_required_raises_error(self, name: str | None) -> None:
        # Given: an empty or missing product name
        # When & Then: should raise a validation error
        with pytest.raises(ProductDomainError, match="required"):
            ProductName(name)  # type: ignore


#####


class TestSKU:
    def test_valid_sku_creates_successfully(self) -> None:
        # Given: a valid SKU
        sku_value = "ABCD-1234"

        # When: creating the SKU
        result = SKU(sku_value)

        # Then: it should store the value
        assert result.value == sku_value

    @pytest.mark.parametrize("sku", ["", None])
    def test_sku_required_raises_error(self, sku: str | None) -> None:
        # Given: an empty or missing SKU
        # When & Then: should raise a validation error
        with pytest.raises(ProductDomainError, match="required"):
            SKU(sku)  # type: ignore

    @pytest.mark.parametrize("sku", ["A1", "ABC"])  # less than 4 chars
    def test_sku_too_short_raises_error(self, sku: str) -> None:
        # Given: a SKU that is too short
        # When & Then: should raise a validation error
        with pytest.raises(ProductDomainError, match="at least"):
            SKU(sku)

    @pytest.mark.parametrize("sku", ["A" * 33, "LONGSKU-123456789012345678901234567890123"])  # more than 32 chars
    def test_sku_too_long_raises_error(self, sku: str) -> None:
        # Given: a SKU that is too long
        # When & Then: should raise a validation error
        with pytest.raises(ProductDomainError, match="at most"):
            SKU(sku)

    @pytest.mark.parametrize("sku", ["abcd1234", "ABC*1234", "abc-DEF"])  # invalid format
    def test_sku_invalid_format_raises_error(self, sku: str) -> None:
        # Given: a SKU with invalid format
        # When & Then: should raise a validation error
        with pytest.raises(ProductDomainError, match="format is invalid"):
            SKU(sku)


class TestSlug:
    def test_valid_slug_creates_successfully(self) -> None:
        # Given: a valid slug value
        value = "valid-slug-123"

        # When: creating the Slug
        result = Slug(value)

        # Then: it should store the value
        assert result.value == value

    @pytest.mark.parametrize("value", ["", None])
    def test_slug_required_raises_error(self, value: str | None) -> None:
        # Given: an empty or missing slug
        # When & Then: should raise a validation error
        with pytest.raises(CatalogDomainError, match="required"):
            Slug(value)  # type: ignore

    @pytest.mark.parametrize(
        "name,expected_slug",
        [
            ("My Product", "my-product"),
            ("Café con leche", "cafe-con-leche"),
            ("  Spaces  Test  ", "spaces-test"),
            ("Symbols!@#", "symbols"),
        ],
    )
    def test_slug_from_name_generates_expected_slug(self, name: str, expected_slug: str) -> None:
        # Given: a product/category name
        # When: converting it to a slug
        result = Slug.from_name(name)

        # Then: it should generate the expected slug
        assert result.value == expected_slug


class TestWeightUnit:
    @pytest.mark.parametrize("unit", ["kg", "g", "lb"])
    def test_valid_weight_unit_creates_successfully(self, unit: str) -> None:
        # Given: a valid weight unit
        # When: creating the WeightUnit
        result = WeightUnit(unit)

        # Then: it should store the value
        assert result.value == unit

    @pytest.mark.parametrize("unit", ["oz", "ml", "", None])
    def test_invalid_weight_unit_raises_error(self, unit: str | None) -> None:
        # Given: an invalid weight unit
        # When & Then: should raise a domain error
        with pytest.raises(ProductDomainError, match="Invalid unit"):
            WeightUnit(unit)  # type: ignore

    def test_default_weight_unit_is_kg(self) -> None:
        # Given: no value provided
        # When: creating the WeightUnit
        result = WeightUnit()

        # Then: default value should be "kg"
        assert result.value == "kg"
