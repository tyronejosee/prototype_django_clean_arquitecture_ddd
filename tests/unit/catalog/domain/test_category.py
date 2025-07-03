from datetime import datetime
from uuid import UUID

import pytest

from apps.catalog.domain.entities import Category
from apps.catalog.domain.exceptions import CategoryDomainException


def valid_category_kwargs(**overrides) -> dict:
    data = dict(
        id=UUID("1a2b3c4d-1a2b-1a2b-1a2b-1a2b3c4d1a2b"),
        name="Category 1",
        description="Category 1 description",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    data.update(overrides)
    return data


def test_category_creation() -> None:
    category = Category(**valid_category_kwargs())
    assert category.name == "Category 1"
    assert category.description == "Category 1 description"
    assert category.is_active is True


def test_category_attributes() -> None:
    category = Category(**valid_category_kwargs())
    for attr in ["name", "description", "is_active", "created_at", "updated_at"]:
        assert hasattr(category, attr)


@pytest.mark.parametrize(
    "invalid_name",
    [
        "",
        "forbidden",
        "badword",
        "invalid",
        "test",
    ],
)
def test_category_creation_invalid_name(invalid_name: str) -> None:
    with pytest.raises(CategoryDomainException):
        Category(**valid_category_kwargs(name=invalid_name))
