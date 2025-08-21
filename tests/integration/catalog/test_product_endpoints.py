import io
from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework.test import APIClient
import pytest

from src.modules.catalog.infrastructure.models.product_model import ProductModel
from src.modules.catalog.infrastructure.models.brand_model import BrandModel
from src.modules.catalog.infrastructure.models.category_model import CategoryModel
from tests.integration.catalog.factories import ProductModelFactory


def generate_test_image_file() -> SimpleUploadedFile:
    """Generate a temporary image in memory for use in tests."""
    # ! TODO: refactor to utils folder
    file = io.BytesIO()
    image = Image.new("RGB", (100, 100), "blue")
    image.save(file, "JPEG")
    file.seek(0)
    return SimpleUploadedFile("test.jpg", file.read(), content_type="image/jpeg")


@pytest.mark.django_db()
class TestListProductsEndpoint:
    def test_returns_empty_when_no_products(self, anon_client: APIClient) -> None:
        # Given: no products exist in the database
        # When: sending a GET request to /products
        url = reverse("catalog:product-list")
        response = anon_client.get(url)

        # Then: response should be 200 OK and empty
        assert response.status_code == 200  # type: ignore
        assert response.data["count"] == 0  # type: ignore


@pytest.mark.django_db()
class TestCreateProductEndpoint:
    def test_requires_admin(self, user_client: APIClient, brand: BrandModel, category: CategoryModel) -> None:
        # Given: an authenticated non-admin user
        url = reverse("catalog:product-list")
        payload = {
            "name": "TestProduct",
            "description": "A product",
            "sku": "TP001",
            "category_id": str(category.id),
            "brand_id": str(brand.id),
            "price": "10.00",
            "stock": 5,
            "min_stock": 1,
            "unit": "kg",
            "is_active": True,
            "is_featured": False,
            "image": generate_test_image_file(),
        }
        # When: they try to POST request to /products
        response = user_client.post(url, payload, format="multipart")

        # Then: forbidden
        assert response.status_code == 403  # type: ignore
        assert ProductModel.objects.count() == 0

    def test_creates_successfully(
        self, superuser_client: APIClient, brand: BrandModel, category: CategoryModel
    ) -> None:
        # Given: an authenticated admin and valid payload for a product
        url = reverse("catalog:product-list")
        payload = {
            "name": "AdminProduct",
            "description": "Desc",
            "sku": "AP001",
            "category_id": str(category.id),
            "brand_id": str(brand.id),
            "price": "20.00",
            "stock": 10,
            "min_stock": 2,
            "unit": "kg",
            "is_active": True,
            "is_featured": True,
            "image": generate_test_image_file(),
        }

        # When: sending a POST request to /products
        response = superuser_client.post(url, payload, format="multipart")

        # Then: the response should be 201 Created and the product should exist in the database
        assert response.status_code == 201  # type: ignore
        assert ProductModel.objects.filter(name="AdminProduct").exists()


@pytest.mark.django_db()
class TestGetProductDetailEndpoint:
    def test_returns_404_for_nonexistent(self, anon_client: APIClient) -> None:
        url = reverse("catalog:product-detail", args=[uuid4()])
        response = anon_client.get(url)
        assert response.status_code == 404  # type: ignore

    def test_returns_product(self, anon_client: APIClient, product: ProductModel) -> None:
        url = reverse("catalog:product-detail", args=[product.id])
        response = anon_client.get(url)
        assert response.status_code == 200  # type: ignore
        assert response.data["name"] == product.name  # type: ignore


@pytest.mark.django_db()
class TestUpdateProductEndpoint:
    def test_updates_successfully(self, superuser_client: APIClient, product: ProductModel) -> None:
        # Given: an existing product in the database
        # When: the admin updates it via PUT request to /products/<id>
        url = reverse("catalog:product-detail", args=[product.id])
        payload = {
            "name": "UpdatedName",
            "description": product.description,
            "sku": product.sku,
            "category_id": str(product.category_id),  # type: ignore
            "brand_id": str(product.brand_id),  # type: ignore
            "image": generate_test_image_file(),
            "price": str(product.price),
            "stock": product.stock,
            "min_stock": product.min_stock,
            "unit": product.unit,
            "is_active": True,
            "is_featured": product.is_featured,
        }
        response = superuser_client.put(url, payload, format="multipart")

        # Then: the response should be 200 OK and the product name should be updated
        product.refresh_from_db()
        assert response.status_code == 200  # type: ignore
        assert product.name == "UpdatedName"


@pytest.mark.django_db()
class TestDeleteProductEndpoint:
    def test_deletes_successfully(self, superuser_client: APIClient, product: ProductModel) -> None:
        # Given: an existing product in the database
        # When: the admin deletes it via DELETE request to /products/<id>
        url = reverse("catalog:product-detail", args=[product.id])
        response = superuser_client.delete(url)

        # Then: the response should be 204 No Content
        assert response.status_code == 204  # type: ignore


@pytest.mark.django_db()
class TestFeaturedProductsEndpoint:
    def test_returns_only_featured(self, anon_client: APIClient) -> None:
        # Given: a featured product and a non-featured product
        featured = ProductModelFactory(name="FeatureOne", is_featured=True)
        ProductModelFactory(name="NotFeatured", is_featured=False)

        # When: sending a GET request to /products/featured
        url = reverse("catalog:featured-products")
        response = anon_client.get(url)

        # Then: the response should be 200 OK and only the featured product should be returned
        assert response.status_code == 200  # type: ignore
        names = [p["name"] for p in response.data["results"]]  # type: ignore
        assert featured.name in names
        assert "NotFeatured" not in names
