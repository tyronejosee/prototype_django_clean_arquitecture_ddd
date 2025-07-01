"""Routers for the catalog presentation"""

from django.urls import path

from apps.catalog.presentation.views import (
    CategoryListCreateView,
    CategoryDetailView,
    CategoryProductListView,
    ProductListCreateView,
    ProductDetailView,
    FeaturedProductsView,
)

app_name = "catalog"

urlpatterns: list = [
    path(
        "categories",
        CategoryListCreateView.as_view(),
        name="category-list",
    ),
    path(
        "categories/<uuid:category_id>",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path(
        "categories/<uuid:category_id>/products",
        CategoryProductListView.as_view(),
        name="products-by-category",
    ),
    path(
        "products",
        ProductListCreateView.as_view(),
        name="product-list",
    ),
    path(
        "products/<uuid:product_id>",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
    path(
        "products/featured",
        FeaturedProductsView.as_view(),
        name="featured-products",
    ),
]
