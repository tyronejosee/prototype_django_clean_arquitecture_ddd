from django.urls import path
from django.urls.resolvers import URLPattern

from src.modules.cart.presentation.controllers.cart_controller import (
    CartController,
)
from src.modules.cart.presentation.controllers.cart_item_controller import (
    CartItemController,
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
]
