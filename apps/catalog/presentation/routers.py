from django.urls import path

from .controllers.category_controller import (
    CategoryDetailController,
    CategoryListCreateController,
    CategoryProductListController,
)
from .controllers.product_controller import (
    FeaturedProductsController,
    ProductDetailController,
    ProductListCreateController,
)

app_name = "catalog"

urlpatterns: list = [
    path(
        "categories",
        CategoryListCreateController.as_view(),
        name="category-list",
    ),
    path(
        "categories/<uuid:category_id>",
        CategoryDetailController.as_view(),
        name="category-detail",
    ),
    path(
        "categories/<uuid:category_id>/products",
        CategoryProductListController.as_view(),
        name="products-by-category",
    ),
    path(
        "products",
        ProductListCreateController.as_view(),
        name="product-list",
    ),
    path(
        "products/<uuid:product_id>",
        ProductDetailController.as_view(),
        name="product-detail",
    ),
    path(
        "products/featured",
        FeaturedProductsController.as_view(),
        name="featured-products",
    ),
]
