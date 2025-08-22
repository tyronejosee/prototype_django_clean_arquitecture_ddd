from datetime import datetime
from decimal import Decimal
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
import pytest

from src.modules.catalog.infrastructure.models.brand_model import BrandModel
from src.modules.catalog.infrastructure.models.category_model import CategoryModel
from src.modules.catalog.infrastructure.models.product_model import ProductModel


@pytest.mark.django_db()
class TestBrandModel:
    def test_brand_model_creation_and_str(self) -> None:
        # Given: data to create a brand
        name = "Nike"
        slug = "nike"

        # When: the brand is created in the database
        brand = BrandModel.objects.create(name=name, slug=slug, is_active=True)

        # Then: the object has an assigned ID and __str__ works correctly
        assert brand.id is not None
        assert brand.name == name
        assert brand.slug == slug
        assert brand.is_active is True
        assert isinstance(brand.created_at, datetime)
        assert isinstance(brand.updated_at, datetime)
        assert str(brand) == name


@pytest.mark.django_db()
class TestCategoryModel:
    def test_category_model_creation_and_str(self) -> None:
        # Given: data to create a category
        name = "Shoes"
        slug = "shoes"
        description = "All kinds of shoes"

        # When: the category is created in the database
        category = CategoryModel.objects.create(name=name, slug=slug, description=description, is_active=True)

        # Then: the object has an assigned ID and __str__ works correctly
        assert category.id is not None
        assert category.name == name
        assert category.slug == slug
        assert category.description == description
        assert category.is_active is True
        assert isinstance(category.created_at, datetime)
        assert isinstance(category.updated_at, datetime)
        assert str(category) == name


@pytest.mark.django_db()
class TestProductModel:
    def test_product_model_creation_and_str(self) -> None:
        # Given: a brand and a category for the product
        brand = BrandModel.objects.create(name="Nike", slug="nike")
        category = CategoryModel.objects.create(name="Shoes", slug="shoes", description="All kinds of shoes")

        # And: data to create the product
        name = "Air Max 90"
        slug = "air-max-90"
        sku = "AM90-001"
        price = Decimal("120.00")
        discount_price = Decimal("100.00")
        stock = 10
        min_stock = 2
        image_content = BytesIO(b"fake image content")
        image_file = SimpleUploadedFile("airmax.jpg", image_content.read(), content_type="image/jpeg")

        # When: the product is created in the database
        product = ProductModel.objects.create(
            name=name,
            slug=slug,
            description="High quality running shoes",
            sku=sku,
            category=category,
            brand=brand,
            price=price,
            discount_price=discount_price,
            stock=stock,
            min_stock=min_stock,
            image=image_file,
            is_active=True,
            is_featured=False,
            weight=1.2,
            unit="kg",
            nutritional_info={"calories": 0},
            ingredients={"material": "leather"},
            allergens=None,
        )

        # Then: the object has an assigned ID and __str__ works correctly
        assert product.id is not None
        assert product.name == name
        assert product.slug == slug
        assert product.sku == sku
        assert product.category == category
        assert product.brand == brand
        assert product.price == price
        assert product.discount_price == discount_price
        assert product.stock == stock
        assert product.min_stock == min_stock
        assert product.is_active is True
        assert product.is_featured is False
        assert product.weight == 1.2
        assert product.unit == "kg"
        assert product.nutritional_info == {"calories": 0}
        assert product.ingredients == {"material": "leather"}
        assert product.allergens is None
        assert isinstance(product.created_at, datetime)
        assert isinstance(product.updated_at, datetime)
        assert str(product) == name
