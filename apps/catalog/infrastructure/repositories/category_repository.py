from uuid import UUID

from apps.catalog.domain.entities.category import Category
from apps.catalog.domain.exceptions import CategoryNotFoundError
from apps.catalog.domain.factories.category_factory import CategoryFactory
from apps.catalog.domain.interfaces.category_repository_interface import (
    CategoryRepositoryInterface,
)
from apps.catalog.infrastructure.models.category_model import CategoryModel


class CategoryRepository(CategoryRepositoryInterface):
    # Messages
    CATEGORY_NOT_FOUND_MSG: str = "Category not found."

    def get_by_id(self, category_id: UUID) -> Category | None:
        try:
            category_model = CategoryModel.objects.get(
                pk=category_id,
                is_active=True,
            )
            return CategoryFactory.from_model(category_model)
        except CategoryModel.DoesNotExist as error:
            raise CategoryNotFoundError(self.CATEGORY_NOT_FOUND_MSG) from error

    def list_all(self) -> list[Category]:
        return [
            CategoryFactory.from_model(category_model)
            for category_model in CategoryModel.objects.filter(
                is_active=True,
            )
        ]

    def create(self, category: Category) -> Category:
        category_model = CategoryModel.objects.create(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
        return CategoryFactory.from_model(category_model)

    def update(self, category_id: UUID, category: Category) -> Category | None:
        updated = CategoryModel.objects.filter(pk=category_id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
        if updated:
            category_model = CategoryModel.objects.get(pk=category_id)
            return CategoryFactory.from_model(category_model)
        return None

    def delete(self, category_id: UUID) -> None:
        try:
            category_model = CategoryModel.objects.get(pk=category_id)
            category_model.is_active = False
            category_model.save()
        except CategoryModel.DoesNotExist as error:
            raise CategoryNotFoundError(self.CATEGORY_NOT_FOUND_MSG) from error

    def exists_by_name(self, name: str) -> bool:
        return CategoryModel.objects.filter(name=name, is_active=True).exists()
