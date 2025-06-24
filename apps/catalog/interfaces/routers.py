"""Routers for the catalog interfaces"""

from django.urls import path

from apps.catalog.interfaces.views import (
    CategoryListView,
    CategoryProductListView,
    ProductListView,
    ProductDetailView,
    FeaturedProductsView,
)

app_name = "catalog"

urlpatterns: list = [
    path(
        "categories",
        CategoryListView.as_view(),
        name="category-list",
    ),
    path(
        "categories/<uuid:category_id>/products",
        CategoryProductListView.as_view(),
        name="products-by-category",
    ),
    path(
        "products",
        ProductListView.as_view(),
        name="product-list",
    ),
    path(
        "products/<uuid:pk>",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
    path(
        "products/featured",
        FeaturedProductsView.as_view(),
        name="featured-products",
    ),
]
