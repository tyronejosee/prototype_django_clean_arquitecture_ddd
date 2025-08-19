from typing import override
from uuid import UUID

from src.modules.catalog.domain.entities.brand import Brand
from src.modules.catalog.domain.exceptions import BrandNotFoundError
from src.modules.catalog.domain.factories.brand_factory import BrandFactory
from src.modules.catalog.domain.interfaces.brand_repository_interface import BrandRepositoryInterface
from src.modules.catalog.infrastructure.models.brand_model import BrandModel


class BrandRepository(BrandRepositoryInterface):
    # Messages
    BRAND_NOT_FOUND_MSG: str = "Brand not found."

    @override
    def get_by_id(self, brand_id: UUID) -> Brand | None:
        try:
            category_model = BrandModel.objects.get(pk=brand_id, is_active=True)
            return BrandFactory.from_model(category_model)
        except BrandModel.DoesNotExist as error:
            raise BrandNotFoundError(self.BRAND_NOT_FOUND_MSG) from error

    @override
    def list_all(self) -> list[Brand]:
        queryset = BrandModel.objects.filter(is_active=True)
        return [BrandFactory.from_model(brand_model) for brand_model in queryset]

    @override
    def create(self, brand: Brand) -> Brand:
        brand_model = BrandModel.objects.create(
            id=brand.id, name=brand.name, slug=brand.slug, is_active=brand.is_active
        )
        return BrandFactory.from_model(brand_model)

    @override
    def update(self, brand_id: UUID, brand: Brand) -> Brand:
        try:
            brand_model = BrandModel.objects.get(pk=brand_id)
            brand_model.name = brand.name.value
            brand_model.slug = brand.slug.value
            brand_model.is_active = brand.is_active
            brand_model.save()
            return BrandFactory.from_model(brand_model)
        except BrandModel.DoesNotExist as error:
            raise BrandNotFoundError(self.BRAND_NOT_FOUND_MSG) from error

    @override
    def delete(self, brand_id: UUID) -> None:
        try:
            brand_model = BrandModel.objects.get(pk=brand_id)
            brand_model.is_active = False
            brand_model.save()
        except BrandModel.DoesNotExist as error:
            raise BrandNotFoundError(self.BRAND_NOT_FOUND_MSG) from error

    @override
    def exists(self, brand_id: UUID) -> bool:
        return BrandModel.objects.filter(pk=brand_id, is_active=True).exists()

    @override
    def exists_by_name(self, name: str) -> bool:
        return BrandModel.objects.filter(name=name, is_active=True).exists()
