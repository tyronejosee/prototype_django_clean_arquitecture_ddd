"""Repositories for the catalog infrastructure"""

from uuid import UUID
from typing import Optional

from django.db.models import Q

from apps.catalog.domain.entities import Category, Product
from apps.catalog.domain.interfaces import (
    CategoryRepositoryInterface,
    ProductRepositoryInterface,
)
from apps.catalog.infrastructure.models import CategoryModel, ProductModel


class CategoryRepository(CategoryRepositoryInterface):
    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        try:
            category_model = CategoryModel.objects.get(
                pk=category_id,
                is_active=True,
            )
            return self._to_entity(category_model)
        except CategoryModel.DoesNotExist:
            return None

    def list_all(self) -> list[Category]:
        return [
            self._to_entity(category_model)
            for category_model in CategoryModel.objects.filter(
                is_active=True,
            )
        ]

    def save(self, category: Category) -> None:
        category_model, _ = CategoryModel.objects.update_or_create(
            pk=category.id,
            defaults={
                "name": category.name,
                "description": category.description,
                "parent_id": category.parent_id,
                "image": category.image_url,
                "is_active": category.is_active,
            },
        )
        category_model.save()

    def delete(self, category_id: UUID) -> None:
        try:
            category_model = CategoryModel.objects.get(pk=category_id)
            category_model.is_active = False
            category_model.save()
        except CategoryModel.DoesNotExist:
            pass

    def _to_entity(self, category_model: CategoryModel) -> Category:
        return Category(
            id=category_model.id,
            name=category_model.name,
            description=category_model.description,
            parent_id=category_model.parent_id,  # type: ignore[attr-defined]
            image_url=category_model.image.url if category_model.image else None,
            is_active=category_model.is_active,
            created_at=category_model.created_at,
            updated_at=category_model.updated_at,
        )


class ProductRepository(ProductRepositoryInterface):
    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        try:
            product_model = ProductModel.objects.get(
                pk=product_id,
                is_active=True,
            )
            return self._to_entity(product_model)
        except ProductModel.DoesNotExist:
            return None

    def list_all(self, filters: dict) -> list[Product]:
        queryset = self._apply_filters(
            ProductModel.objects.filter(is_active=True), filters
        )
        return [self._to_entity(product_model) for product_model in queryset]

    def save(self, product: Product) -> None:
        product_model, _ = ProductModel.objects.update_or_create(
            pk=product.id,
            defaults={
                "name": product.name,
                "description": product.description,
                "sku": product.sku,
                "category_id": product.category_id,
                "price": product.price,
                "discount_price": product.discount_price,
                "stock": product.stock,
                "min_stock": product.min_stock,
                "image": product.image_url,
                "is_active": product.is_active,
                "is_featured": product.is_featured,
                "weight": product.weight,
                "unit": product.unit,
            },
        )
        product_model.save()

    def delete(self, product_id: UUID) -> None:
        try:
            product_model = ProductModel.objects.get(pk=product_id)
            product_model.is_active = False
            product_model.save()
        except ProductModel.DoesNotExist:
            pass

    def list_featured(self) -> list[Product]:
        return [
            self._to_entity(product_model)
            for product_model in ProductModel.objects.filter(
                is_featured=True,
                is_active=True,
            )
        ]

    def list_by_category(self, category_id: UUID) -> list[Product]:
        return [
            self._to_entity(product_model)
            for product_model in ProductModel.objects.filter(
                category_id=category_id,
                is_active=True,
            )
        ]

    def _apply_filters(self, queryset, filters: dict):
        q = filters.get("q", None)
        category_id = filters.get("category", None)
        min_price = filters.get("min_price", None)
        max_price = filters.get("max_price", None)

        if q:
            queryset = queryset.filter(Q(name__icontains=q))
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.distinct()

    def _to_entity(self, product_model: ProductModel) -> Product:
        return Product(
            id=product_model.id,
            name=product_model.name,
            description=product_model.description,
            sku=product_model.sku,
            category_id=product_model.category_id,  # type: ignore[attr-defined]
            price=product_model.price,
            discount_price=product_model.discount_price,
            stock=product_model.stock,
            min_stock=product_model.min_stock,
            image_url=product_model.image.url if product_model.image else None,
            is_active=product_model.is_active,
            is_featured=product_model.is_featured,
            weight=product_model.weight,
            unit=product_model.unit,
            created_at=product_model.created_at,
            updated_at=product_model.updated_at,
        )
