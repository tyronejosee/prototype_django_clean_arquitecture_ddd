from django.urls import path

from src.modules.catalog.presentation.controllers.brand_controller import (
    BrandDetailController,
    BrandListCreateController,
    BrandProductListController,
)
from src.modules.catalog.presentation.controllers.category_controller import (
    CategoryDetailController,
    CategoryListCreateController,
    CategoryProductListController,
)
from src.modules.catalog.presentation.controllers.product_controller import (
    FeaturedProductsController,
    ProductDetailController,
    ProductListCreateController,
)

app_name = "catalog"

urlpatterns: list = [
    path("brands", BrandListCreateController.as_view(), name="brand-list"),
    path("brands/<uuid:brand_id>", BrandDetailController.as_view(), name="brand-detail"),
    path("brands/<uuid:brand_id>/products", BrandProductListController.as_view(), name="products-by-brand"),
    path("categories", CategoryListCreateController.as_view(), name="category-list"),
    path("categories/<uuid:category_id>", CategoryDetailController.as_view(), name="category-detail"),
    path(
        "categories/<uuid:category_id>/products", CategoryProductListController.as_view(), name="products-by-category"
    ),
    path("products", ProductListCreateController.as_view(), name="product-list"),
    path("products/<uuid:product_id>", ProductDetailController.as_view(), name="product-detail"),
    path("products/featured", FeaturedProductsController.as_view(), name="featured-products"),
]
