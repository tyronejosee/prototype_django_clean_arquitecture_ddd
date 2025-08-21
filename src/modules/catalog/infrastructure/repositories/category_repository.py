from typing import override
from uuid import UUID

from src.modules.catalog.domain.entities.category import Category
from src.modules.catalog.domain.exceptions import CategoryNotFoundError
from src.modules.catalog.domain.factories.category_factory import CategoryFactory
from src.modules.catalog.domain.interfaces.category_repository_interface import CategoryRepositoryInterface
from src.modules.catalog.infrastructure.models.category_model import CategoryModel


class CategoryRepository(CategoryRepositoryInterface):
    # Messages
    CATEGORY_NOT_FOUND_MSG: str = "Category not found."

    @override
    def get_by_id(self, category_id: UUID) -> Category | None:
        try:
            category_model = CategoryModel.objects.get(pk=category_id, is_active=True)
            return CategoryFactory.from_model(category_model)
        except CategoryModel.DoesNotExist as error:
            raise CategoryNotFoundError(self.CATEGORY_NOT_FOUND_MSG) from error

    @override
    def list_all(self) -> list[Category]:
        queryset = CategoryModel.objects.filter(is_active=True)
        return [CategoryFactory.from_model(category_model) for category_model in queryset]

    @override
    def create(self, category: Category) -> Category:
        category_model = CategoryModel.objects.create(
            id=category.id,
            name=category.name,
            slug=category.slug,
            description=category.description,
            is_active=category.is_active,
        )
        return CategoryFactory.from_model(category_model)

    @override
    def update(self, category_id: UUID, category: Category) -> Category:
        try:
            category_model = CategoryModel.objects.get(pk=category_id)
            category_model.name = category.name.value
            category_model.slug = category.slug.value
            category_model.description = category.description
            category_model.is_active = category.is_active
            category_model.save()
            return CategoryFactory.from_model(category_model)
        except CategoryModel.DoesNotExist as error:
            raise CategoryNotFoundError(self.CATEGORY_NOT_FOUND_MSG) from error

    @override
    def delete(self, category_id: UUID) -> None:
        try:
            category_model = CategoryModel.objects.get(pk=category_id)
            category_model.is_active = False
            category_model.save()
        except CategoryModel.DoesNotExist as error:
            raise CategoryNotFoundError(self.CATEGORY_NOT_FOUND_MSG) from error

    @override
    def exists(self, category_id: UUID) -> bool:
        return CategoryModel.objects.filter(pk=category_id, is_active=True).exists()

    @override
    def exists_by_name(self, name: str) -> bool:
        return CategoryModel.objects.filter(name=name, is_active=True).exists()
