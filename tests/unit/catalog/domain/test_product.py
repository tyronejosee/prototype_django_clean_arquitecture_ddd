import pytest
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from apps.catalog.domain.entities import Product
from apps.catalog.domain.exceptions import ProductDomainException


def valid_product_kwargs(**overrides) -> dict:
    data = dict(
        id=UUID("2b3c4d5e-2b3c-2b3c-2b3c-2b3c4d5e2b3c"),
        name="Test Product",
        description="Test description",
        sku="SKU123",
        category_id=UUID("1a2b3c4d-1a2b-1a2b-1a2b-1a2b3c4d1a2b"),
        price=Decimal("10.0"),
        discount_price=None,
        stock=10,
        min_stock=5,
        image_url=None,
        is_active=True,
        is_featured=False,
        weight=None,
        unit="kg",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    data.update(overrides)
    return data


def test_product_creation() -> None:
    product = Product(**valid_product_kwargs())
    assert product.name == "Test Product"
    assert product.price == Decimal("10.0")
    assert product.sku == "SKU123"
    assert product.stock == 10
    assert product.is_active is True
    assert product.unit == "kg"


def test_product_update_price() -> None:
    product = Product(**valid_product_kwargs())
    product.price = Decimal("15.0")
    assert product.price == Decimal("15.0")


def test_product_attributes() -> None:
    product = Product(**valid_product_kwargs())
    for attr in [
        "name",
        "price",
        "description",
        "sku",
        "category_id",
        "stock",
        "min_stock",
        "image_url",
        "is_active",
        "is_featured",
        "weight",
        "unit",
    ]:
        assert hasattr(product, attr)


@pytest.mark.parametrize(
    "invalid_price",
    [
        Decimal("-1.0"),
        Decimal("-100.0"),
        Decimal("-0.01"),
    ],
)
def test_product_price_validation(invalid_price: Decimal) -> None:
    with pytest.raises(ProductDomainException):
        Product(**valid_product_kwargs(price=invalid_price))


@pytest.mark.parametrize(
    "invalid_discount",
    [
        Decimal("-1.0"),
        Decimal("-100.0"),
    ],
)
def test_product_discount_price_negative(invalid_discount: Decimal) -> None:
    with pytest.raises(ProductDomainException):
        Product(**valid_product_kwargs(discount_price=invalid_discount))


def test_product_discount_price_greater_than_price() -> None:
    with pytest.raises(ProductDomainException):
        Product(
            **valid_product_kwargs(
                price=Decimal("10.0"),
                discount_price=Decimal("20.0"),
            ),
        )


@pytest.mark.parametrize(
    "invalid_stock",
    [-1, -100],
)
def test_product_stock_negative(invalid_stock: int) -> None:
    with pytest.raises(ProductDomainException):
        Product(**valid_product_kwargs(stock=invalid_stock))


def test_product_stock_too_high() -> None:
    with pytest.raises(ProductDomainException):
        Product(**valid_product_kwargs(stock=101))


@pytest.mark.parametrize(
    "invalid_min_stock",
    [-1, -10],
)
def test_product_min_stock_negative(invalid_min_stock: int) -> None:
    with pytest.raises(ProductDomainException):
        Product(**valid_product_kwargs(min_stock=invalid_min_stock))


def test_product_name_required() -> None:
    with pytest.raises(ProductDomainException):
        Product(**valid_product_kwargs(name=""))
