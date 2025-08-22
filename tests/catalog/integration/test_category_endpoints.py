from django.urls import reverse
from rest_framework.test import APIClient
import pytest

from src.modules.catalog.infrastructure.models.category_model import CategoryModel
from tests.catalog.factories import CategoryModelFactory


@pytest.mark.django_db()
class TestListCategoriesEndpoint:
    def test_returns_paginated_categories(self, anon_client: APIClient) -> None:
        # Given: two categories exist in the database
        CategoryModelFactory.create_batch(2)

        # When: sending a GET request to the /categories endpoint
        url = reverse("catalog:category-list")
        response = anon_client.get(url)

        # Then: the response should be 200 OK and return both categories paginated
        assert response.status_code == 200  # type: ignore
        assert response.data["count"] == 2  # type: ignore


@pytest.mark.django_db()
class TestCreateCategoryEndpoint:
    def test_requires_admin(self, user_client: APIClient) -> None:
        # Given: an authenticated non-admin user
        # When: they try to POST a new category
        url = reverse("catalog:category-list")
        response = user_client.post(
            url, {"name": "NewCategory", "description": "Test desc", "is_active": True}, format="json"
        )

        # Then: the response should be 403 Forbidden and no category should be created
        assert response.status_code == 403  # type: ignore
        assert CategoryModel.objects.count() == 0

    def test_creates_category_successfully(self, superuser_client: APIClient) -> None:
        # Given: an authenticated admin user
        # When: they POST a valid category
        url = reverse("catalog:category-list")
        response = superuser_client.post(
            url, {"name": "AdminCategory", "description": "Admin desc", "is_active": True}, format="json"
        )

        # Then: the response should be 201 Created and the category should exist in the database
        assert response.status_code == 201  # type: ignore
        assert CategoryModel.objects.filter(name="AdminCategory").exists()


@pytest.mark.django_db()
class TestUpdateCategoryEndpoint:
    def test_updates_successfully(self, superuser_client: APIClient) -> None:
        # Given: an existing category in the database
        category = CategoryModel.objects.create(name="Old Name", slug="old-name", description="Old desc")

        # When: the admin updates it via PUT
        url = reverse("catalog:category-detail", args=[category.id])
        response = superuser_client.put(
            url, {"name": "New Name", "description": "New desc", "is_active": True}, format="json"
        )

        # Then: the response should be 200 OK and the category name should be updated
        category.refresh_from_db()
        assert response.status_code == 200  # type: ignore
        assert category.name == "New Name"
        assert category.description == "New desc"


@pytest.mark.django_db()
class TestDeleteCategoryEndpoint:
    def test_marks_inactive(self, superuser_client: APIClient) -> None:
        # Given: an active category exists in the database
        category = CategoryModel.objects.create(name="ToDelete", slug="to-delete", description="to be deleted")

        # When: the admin deletes it via DELETE
        url = reverse("catalog:category-detail", args=[category.id])
        response = superuser_client.delete(url)

        # Then: the response should be 204 No Content and the category should be marked inactive
        category.refresh_from_db()
        assert response.status_code == 204  # type: ignore
        assert category.is_active is False


@pytest.mark.django_db()
class TestListProductsByCategoryEndpoint:
    def test_returns_empty_list_when_no_products(self, anon_client: APIClient, category: CategoryModel) -> None:
        # Given: a category exists with no products
        # When: sending a GET request to /categories/<id>/products
        url = reverse("catalog:products-by-category", args=[category.id])
        response = anon_client.get(url)

        # Then: the response should be 200 OK and the result list should be empty
        assert response.status_code == 200  # type: ignore
        assert response.data["count"] == 0  # type: ignore
