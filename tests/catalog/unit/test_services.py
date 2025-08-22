from decimal import Decimal

import pytest

from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.exceptions import ProductDomainError
from src.modules.catalog.domain.services.product_service import ProductService
from tests.catalog.unit.test_entities import build_valid_product


@pytest.fixture
def product_service() -> ProductService:
    return ProductService()


@pytest.fixture
def active_product() -> Product:
    return build_valid_product(
        name="Test Product",
        price=Decimal("150"),
        stock=20,
        is_active=True,
    )


@pytest.fixture
def inactive_product() -> Product:
    return build_valid_product(
        name="Inactive Product",
        price=Decimal("50"),
        stock=0,
        is_active=False,
    )


class TestProductService:

    # is_active method
    def test_is_active_returns_true(self, product_service: ProductService, active_product: Product) -> None:
        # Given: an active product with stock > 0
        # When: we check if the product is active
        # Then: the result should be True
        result = product_service.is_active(active_product)
        assert result is True

    def test_is_active_returns_false_when_inactive(
        self, product_service: ProductService, inactive_product: Product
    ) -> None:
        # Given: an inactive product
        # When: we check if the product is active
        # Then: the result should be False
        result = product_service.is_active(inactive_product)
        assert result is False

    # check_stock method
    def test_check_stock_sufficient(self, product_service: ProductService, active_product: Product) -> None:
        # Given: a product with stock 20
        # When: we check stock for 10 units
        # Then: it should return True
        result = product_service.check_stock(active_product, 10)
        assert result is True

    def test_check_stock_insufficient(self, product_service: ProductService, active_product: Product) -> None:
        # Given: a product with stock 20
        # When: we check stock for 30 units
        # Then: it should return False
        result = product_service.check_stock(active_product, 30)
        assert result is False

    # can_be_featured method
    def test_can_be_featured_true(self, product_service: ProductService, active_product: Product) -> None:
        # Given: an active product with stock > FEATURED_MIN_STOCK and price > FEATURED_MIN_PRICE
        # When: we check if it can be featured
        # Then: it should return True
        result = product_service.can_be_featured(active_product)
        assert result is True

    def test_can_be_featured_false_due_to_stock(self, product_service, active_product: Product) -> None:
        # Given: an active product with stock <= FEATURED_MIN_STOCK
        active_product.stock = 5
        # When: we check if it can be featured
        # Then: it should return False
        result = product_service.can_be_featured(active_product)
        assert result is False

    def test_can_be_featured_false_due_to_price(self, product_service, active_product: Product) -> None:
        # Given: an active product with price <= FEATURED_MIN_PRICE
        active_product.price = Decimal("50")
        # When: we check if it can be featured
        # Then: it should return False
        result = product_service.can_be_featured(active_product)
        assert result is False

    # restock tests
    def test_restock_success(self, product_service: ProductService, active_product: Product) -> None:
        # Given: a product with stock 20
        # When: we restock 10 units
        # Then: stock should increase to 30
        product_service.restock(active_product, 10)
        assert active_product.stock == 30

    def test_restock_invalid_quantity_raises(self, product_service: ProductService, active_product: Product) -> None:
        # Given: a product
        # When: we try to restock with quantity < MIN_RESTOCK_QUANTITY
        # Then: it should raise ProductDomainError
        with pytest.raises(ProductDomainError) as exc:
            product_service.restock(active_product, 0)
        assert str(exc.value) == ProductService.INVALID_RESTOCK_MSG

    # apply_discount tests
    def test_apply_discount_success(self, product_service: ProductService, active_product: Product) -> None:
        # Given: a product with price 150
        # When: we apply a discount of 10%
        # Then: the discounted price should be 135
        discounted_price = product_service.apply_discount(active_product, 10)
        assert discounted_price == Decimal("135")

    def test_apply_discount_invalid_raises(self, product_service: ProductService, active_product: Product) -> None:
        # Given: a product with price 150
        # When: we apply a discount outside valid range
        # Then: it should raise ProductDomainError
        with pytest.raises(ProductDomainError) as exc:
            product_service.apply_discount(active_product, 200)
        assert str(exc.value) == ProductService.INVALID_DISCOUNT_MSG.format(min_=0, max_=100)
