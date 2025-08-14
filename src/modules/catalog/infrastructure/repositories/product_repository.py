from typing import override
from uuid import UUID

from django.db.models import Q

from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.exceptions import ProductNotFoundError
from src.modules.catalog.domain.factories.product_factory import ProductFactory
from src.modules.catalog.domain.interfaces.product_repository_interface import ProductRepositoryInterface
from src.modules.catalog.infrastructure.models.product_model import ProductModel


class ProductRepository(ProductRepositoryInterface):
    # Messages
    PRODUCT_NOT_FOUND_MSG: str = "Product not found."

    @override
    def get_by_id(self, product_id: UUID) -> Product | None:
        try:
            product_model = ProductModel.objects.get(pk=product_id, is_active=True)
            return ProductFactory.from_model(product_model)
        except ProductModel.DoesNotExist as error:
            raise ProductNotFoundError(self.PRODUCT_NOT_FOUND_MSG) from error

    @override
    def list_all(self, query_params: dict) -> list[Product]:
        queryset = self._apply_filters(ProductModel.objects.filter(is_active=True), query_params)
        return [ProductFactory.from_model(product_model) for product_model in queryset]

    @override
    def create(self, product: Product) -> Product:
        product_model = ProductModel.objects.create(
            id=product.id,
            name=product.name,
            description=product.description,
            sku=product.sku,
            category_id=product.category_id,
            price=product.price,
            discount_price=product.discount_price,
            stock=product.stock,
            min_stock=product.min_stock,
            image=product.image_url,
            is_active=product.is_active,
            is_featured=product.is_featured,
            weight=product.weight,
            unit=product.unit,
        )
        return ProductFactory.from_model(product_model)

    @override
    def update(self, product_id: UUID, product: Product) -> Product:
        try:
            product_model = ProductModel.objects.get(pk=product_id)
            product_model.name = product.name
            product_model.description = product.description
            product_model.sku = product.sku.value
            product_model.category_id = product.category_id  # type: ignore[union-attr]
            product_model.price = product.price
            product_model.discount_price = product.discount_price
            product_model.stock = product.stock
            product_model.min_stock = product.min_stock
            product_model.image = product.image_url  # type: ignore[union-attr]
            product_model.is_active = product.is_active
            product_model.is_featured = product.is_featured
            product_model.weight = product.weight
            product_model.unit = product.unit.value
            product_model.save()
            return ProductFactory.from_model(product_model)
        except ProductModel.DoesNotExist as error:
            raise ProductNotFoundError(self.PRODUCT_NOT_FOUND_MSG) from error

    @override
    def delete(self, product_id: UUID) -> None:
        try:
            product_model = ProductModel.objects.get(pk=product_id)
            product_model.is_active = False
            product_model.save()
        except ProductModel.DoesNotExist as error:
            raise ProductNotFoundError(self.PRODUCT_NOT_FOUND_MSG) from error

    @override
    def exists(self, product_id: UUID) -> bool:
        return ProductModel.objects.filter(pk=product_id, is_active=True).exists()

    @override
    def list_featured(self) -> list[Product]:
        queryset = ProductModel.objects.filter(is_featured=True, is_active=True)
        return [ProductFactory.from_model(product_model) for product_model in queryset]

    @override
    def list_by_category(self, category_id: UUID) -> list[Product]:
        queryset = ProductModel.objects.filter(category_id=category_id, is_active=True)
        return [ProductFactory.from_model(product_model) for product_model in queryset]

    def _apply_filters(self, queryset, filters: dict) -> list[Product]:
        q = filters.get("q")
        category_id = filters.get("category")
        min_price = filters.get("min_price")
        max_price = filters.get("max_price")

        if q:
            queryset = queryset.filter(Q(name__icontains=q))
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.distinct()
