"""Repositories for the catalog infrastructure"""

from uuid import UUID
from typing import Optional

from apps.catalog.domain.models import Category, Product
from apps.catalog.domain.interfaces import (
    CategoryRepositoryInterface,
    ProductRepositoryInterface,
)
from apps.catalog.infrastructure.models import CategoryModel, ProductModel


class CategoryRepository(CategoryRepositoryInterface):

    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        try:
            cm = CategoryModel.objects.get(pk=category_id, is_active=True)
            return self._to_domain(cm)
        except CategoryModel.DoesNotExist:
            return None

    def list_all(self) -> list[Category]:
        return [
            self._to_domain(cm)
            for cm in CategoryModel.objects.filter(
                is_active=True,
            )
        ]

    def save(self, category: Category) -> None:
        cm, _ = CategoryModel.objects.update_or_create(
            pk=category.id,
            defaults={
                "name": category.name,
                "description": category.description,
                "parent_id": category.parent_id,
                "image": category.image_url,
                "is_active": category.is_active,
            },
        )
        cm.save()

    def delete(self, category_id: UUID) -> None:
        try:
            cm = CategoryModel.objects.get(pk=category_id)
            cm.is_active = False
            cm.save()
        except CategoryModel.DoesNotExist:
            pass

    def _to_domain(self, cm: CategoryModel) -> Category:
        return Category(
            id=cm.id,
            name=cm.name,
            description=cm.description,
            parent_id=cm.parent_id,  # type: ignore[attr-defined]
            image_url=cm.image.url if cm.image else None,
            is_active=cm.is_active,
            created_at=cm.created_at,
            updated_at=cm.updated_at,
        )


class ProductRepository(ProductRepositoryInterface):

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        try:
            pm = ProductModel.objects.get(pk=product_id, is_active=True)
            return self._to_domain(pm)
        except ProductModel.DoesNotExist:
            return None

    def list_all(self) -> list[Product]:
        return [
            self._to_domain(pm)
            for pm in ProductModel.objects.filter(
                is_active=True,
            )
        ]

    def save(self, product: Product) -> None:
        pm, _ = ProductModel.objects.update_or_create(
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
        pm.save()

    def delete(self, product_id: UUID) -> None:
        try:
            pm = ProductModel.objects.get(pk=product_id)
            pm.is_active = False
            pm.save()
        except ProductModel.DoesNotExist:
            pass

    def list_featured(self) -> list[Product]:
        return [
            self._to_domain(pm)
            for pm in ProductModel.objects.filter(
                is_featured=True,
                is_active=True,
            )
        ]

    def list_by_category(self, category_id: UUID) -> list[Product]:
        return [
            self._to_domain(pm)
            for pm in ProductModel.objects.filter(
                category_id=category_id,
                is_active=True,
            )
        ]

    def _to_domain(self, pm: ProductModel) -> Product:
        return Product(
            id=pm.id,
            name=pm.name,
            description=pm.description,
            sku=pm.sku,
            category_id=pm.category_id,  # type: ignore[attr-defined] # noqa
            price=pm.price,
            discount_price=pm.discount_price,
            stock=pm.stock,
            min_stock=pm.min_stock,
            image_url=pm.image.url if pm.image else None,
            is_active=pm.is_active,
            is_featured=pm.is_featured,
            weight=pm.weight,
            unit=pm.unit,
            created_at=pm.created_at,
            updated_at=pm.updated_at,
        )
