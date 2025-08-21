from datetime import UTC, datetime
from decimal import Decimal
from typing import cast
from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile

from src.modules.catalog.presentation.serializers.brand_serializer import BrandInputSerializer, BrandOutputSerializer
from src.modules.catalog.presentation.serializers.category_serializer import (
    CategoryInputSerializer,
    CategoryOutputSerializer,
)
from src.modules.catalog.presentation.serializers.product_serializer import (
    ProductInputSerializer,
    ProductOutputSerializer,
)


class TestBrandInputSerializer:
    def test_valid_data_returns_expected_fields(self) -> None:
        # Given: valid input brand data
        data = {"name": "Nike", "is_active": True}

        # When: serializing the input
        serializer = BrandInputSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)

        # Then: output should match input
        assert result["name"] == "Nike"
        assert result["is_active"] is True


class TestBrandOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Given: valid output brand data
        data = {
            "id": uuid4(),
            "name": "Adidas",
            "slug": "adidas",
            "is_active": False,
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
        }

        # When: serializing the output
        serializer = BrandOutputSerializer(instance=data)
        result = cast(dict, serializer.data)

        # Then: output should match input
        assert result["id"] == str(data["id"])
        assert result["name"] == "Adidas"
        assert result["slug"] == "adidas"
        assert result["is_active"] is False
        assert result["created_at"] == data["created_at"].isoformat().replace("+00:00", "Z")
        assert result["updated_at"] == data["updated_at"].isoformat().replace("+00:00", "Z")


class TestCategoryInputSerializer:
    def test_valid_data_returns_expected_fields(self) -> None:
        # Given: valid input category data
        data = {
            "name": "Electronics",
            "description": "Devices and gadgets",
            "is_active": True,
        }

        # When: serializing the input
        serializer = CategoryInputSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)

        # Then: output should match input
        assert result["name"] == "Electronics"
        assert result["description"] == "Devices and gadgets"
        assert result["is_active"] is True


class TestCategoryOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Given: valid output category data
        data = {
            "id": uuid4(),
            "name": "Books",
            "slug": "books",
            "description": "Printed and digital books",
            "is_active": False,
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
        }

        # When: serializing the output
        serializer = CategoryOutputSerializer(instance=data)
        result = cast(dict, serializer.data)

        # Then: output should match input
        assert result["id"] == str(data["id"])
        assert result["name"] == "Books"
        assert result["slug"] == "books"
        assert result["description"] == "Printed and digital books"
        assert result["is_active"] is False
        assert result["created_at"] == data["created_at"].isoformat().replace("+00:00", "Z")
        assert result["updated_at"] == data["updated_at"].isoformat().replace("+00:00", "Z")


class TestProductInputSerializer:
    def test_valid_data_returns_expected_fields(self) -> None:
        # Given: valid input product data
        image = SimpleUploadedFile(
            name="test_image.gif",
            content=(
                b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!"
                b"\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00"
                b"\x00\x02\x02D\x01\x00;"
            ),
            content_type="image/gif",
        )
        data = {
            "name": "Chocolate Bar",
            "description": "Delicious dark chocolate",
            "sku": "CHOC123",
            "category_id": uuid4(),
            "brand_id": uuid4(),
            "price": "3.50",
            "discount_price": "2.99",
            "currency": "USD",
            "stock": 100,
            "min_stock": 10,
            "warehouse_location": "A1",
            "image": image,
            "is_active": True,
            "is_featured": False,
            "weight": "0.150",
            "unit": "kg",
            "nutritional_info": {"calories": 250},
            "ingredients": ["cocoa", "sugar"],
            "allergens": ["nuts"],
        }

        # When: serializing the input
        serializer = ProductInputSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)

        # Then: output should match input
        assert result["name"] == "Chocolate Bar"
        assert result["sku"] == "CHOC123"
        assert Decimal(result["price"]) == Decimal("3.50")
        assert result["is_active"] is True
        assert result["weight"] == Decimal("0.150")
        assert result["nutritional_info"]["calories"] == 250


class TestProductOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Given: valid output product data
        data = {
            "id": uuid4(),
            "name": "Chocolate Bar",
            "slug": "chocolate-bar",
            "description": "Delicious dark chocolate",
            "sku": "CHOC123",
            "category_id": uuid4(),
            "brand_id": uuid4(),
            "price": Decimal("3.50"),
            "discount_price": Decimal("2.99"),
            "currency": "USD",
            "stock": 100,
            "min_stock": 10,
            "warehouse_location": "A1",
            "image_url": "http://testserver/media/example.jpg",
            "is_active": True,
            "is_featured": False,
            "weight": Decimal("0.150"),
            "unit": "kg",
            "nutritional_info": {"calories": 250},
            "ingredients": ["cocoa", "sugar"],
            "allergens": ["nuts"],
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
        }

        # When: serializing the output
        serializer = ProductOutputSerializer(instance=data)
        result = cast(dict, serializer.data)

        # Then: output should match input
        assert result["id"] == str(data["id"])
        assert result["name"] == "Chocolate Bar"
        assert result["slug"] == "chocolate-bar"
        assert result["sku"] == "CHOC123"
        assert Decimal(result["price"]) == Decimal("3.50")
        assert Decimal(result["discount_price"]) == Decimal("2.99")
        assert result["is_active"] is True
        assert Decimal(result["weight"]) == Decimal("0.150")
        assert result["nutritional_info"]["calories"] == 250
        assert result["created_at"] == data["created_at"].isoformat().replace("+00:00", "Z")
        assert result["updated_at"] == data["updated_at"].isoformat().replace("+00:00", "Z")
