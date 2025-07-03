"""Repositories for the catalog infrastructure"""

from uuid import UUID

from django.db.models import Q

from apps.catalog.domain.entities import Category, Product
from apps.catalog.domain.factories.category_factory import CategoryFactory
from apps.catalog.domain.factories.product_factory import ProductFactory
from apps.catalog.domain.interfaces import (
    CategoryRepositoryInterface,
    ProductRepositoryInterface,
)
from apps.catalog.infrastructure.models import CategoryModel, ProductModel


class CategoryRepository(CategoryRepositoryInterface):
    def get_by_id(self, category_id: UUID) -> Category | None:
        try:
            category_model = CategoryModel.objects.get(
                pk=category_id,
                is_active=True,
            )
            return CategoryFactory.from_model(category_model)
        except CategoryModel.DoesNotExist:
            return None

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
        except CategoryModel.DoesNotExist:
            pass

    def exists_by_name(self, name: str) -> bool:
        return CategoryModel.objects.filter(name=name, is_active=True).exists()


class ProductRepository(ProductRepositoryInterface):
    def get_by_id(self, product_id: UUID) -> Product | None:
        try:
            product_model = ProductModel.objects.get(
                pk=product_id,
                is_active=True,
            )
            return ProductFactory.from_model(product_model)
        except ProductModel.DoesNotExist:
            return None

    def list_all(self, filters: dict) -> list[Product]:
        queryset = self._apply_filters(
            ProductModel.objects.filter(is_active=True),
            filters,
        )
        return [ProductFactory.from_model(product_model) for product_model in queryset]

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

    def update(self, product_id: UUID, product: Product) -> Product | None:
        updated = ProductModel.objects.filter(pk=product_id).update(
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
        if updated:
            product_model = ProductModel.objects.get(pk=product_id)
            return ProductFactory.from_model(product_model)
        return None

    def delete(self, product_id: UUID) -> None:
        try:
            product_model = ProductModel.objects.get(pk=product_id)
            product_model.is_active = False
            product_model.save()
        except ProductModel.DoesNotExist:
            pass

    def list_featured(self) -> list[Product]:
        return [
            ProductFactory.from_model(product_model)
            for product_model in ProductModel.objects.filter(
                is_featured=True,
                is_active=True,
            )
        ]

    def list_by_category(self, category_id: UUID) -> list[Product]:
        return [
            ProductFactory.from_model(product_model)
            for product_model in ProductModel.objects.filter(
                category_id=category_id,
                is_active=True,
            )
        ]

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
