from django.urls import path
from django.urls.resolvers import URLPattern

from apps.cart.presentation.controllers.cart_controller import (
    CartController,
)
from apps.cart.presentation.controllers.cart_item_controller import (
    CartItemController,
)
from apps.cart.presentation.controllers.cart_preview_controller import (
    CartPreviewController,
)

app_name = "cart"

urlpatterns: list[URLPattern] = [
    path(
        "cart",
        CartController.as_view(),
        name="cart-main",
    ),
    path(
        "cart/items/<uuid:item_id>",
        CartItemController.as_view(),
        name="cart-item",
    ),
    path(
        "cart/preview",
        CartPreviewController.as_view(),
        name="cart-preview",
    ),
]
