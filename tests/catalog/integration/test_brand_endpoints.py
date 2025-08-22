from django.urls import reverse
from rest_framework.test import APIClient
import pytest

from src.modules.catalog.infrastructure.models.brand_model import BrandModel
from tests.catalog.factories import BrandModelFactory


@pytest.mark.django_db()
class TestListBrandsEndpoint:
    def test_returns_paginated_brands(self, anon_client: APIClient) -> None:
        # Given: two brands exist in the database
        BrandModelFactory.create_batch(2)

        # When: sending a GET request to the /brands endpoint
        url = reverse("catalog:brand-list")
        response = anon_client.get(url)

        # Then: the response should be 200 OK and return both brands paginated
        assert response.status_code == 200  # type: ignore
        assert response.data["count"] == 2  # type: ignore


@pytest.mark.django_db()
class TestCreateBrandEndpoint:
    def test_requires_admin(self, user_client: APIClient) -> None:
        # Given: an authenticated non-admin user
        # When: they try to POST a new brand
        url = reverse("catalog:brand-list")
        response = user_client.post(url, {"name": "NewBrand", "is_active": True}, format="json")

        # Then: the response should be 403 Forbidden and no brand should be created
        assert response.status_code == 403  # type: ignore
        assert BrandModel.objects.count() == 0

    def test_creates_brand_successfully(self, superuser_client: APIClient) -> None:
        # Given: an authenticated admin user
        # When: they POST a valid brand
        url = reverse("catalog:brand-list")
        response = superuser_client.post(url, {"name": "AdminBrand", "is_active": True}, format="json")

        # Then: the response should be 201 Created and the brand should exist in the database
        assert response.status_code == 201  # type: ignore
        assert BrandModel.objects.filter(name="AdminBrand").exists()


@pytest.mark.django_db()
class TestUpdateBrandEndpoint:
    def test_updates_successfully(self, superuser_client: APIClient, brand: BrandModel) -> None:
        # Given: an existing brand in the database
        # When: the admin updates it via PUT
        url = reverse("catalog:brand-detail", args=[brand.id])
        response = superuser_client.put(url, {"name": "New Name", "is_active": True}, format="json")

        # Then: the response should be 200 OK and the brand name should be updated
        brand.refresh_from_db()
        assert response.status_code == 200  # type: ignore
        assert brand.name == "New Name"


@pytest.mark.django_db()
class TestDeleteBrandEndpoint:
    def test_marks_inactive(self, superuser_client: APIClient, brand: BrandModel) -> None:
        # Given: an active brand exists in the database
        # When: the admin deletes it via DELETE
        url = reverse("catalog:brand-detail", args=[brand.id])
        response = superuser_client.delete(url)

        # Then: the response should be 204 No Content and the brand should be marked inactive
        brand.refresh_from_db()
        assert response.status_code == 204  # type: ignore
        assert brand.is_active is False


@pytest.mark.django_db()
class TestListProductsByBrandEndpoint:
    def test_returns_empty_list_when_no_products(self, anon_client: APIClient, brand: BrandModel) -> None:
        # Given: a brand exists with no products
        # When: sending a GET request to /brands/<id>/products
        url = reverse("catalog:products-by-brand", args=[brand.id])
        response = anon_client.get(url)

        # Then: the response should be 200 OK and the result list should be empty
        assert response.status_code == 200  # type: ignore
        assert response.data["count"] == 0  # type: ignore
