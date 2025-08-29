from django.urls import path
from django.urls.resolvers import URLPattern

from src.modules.orders.presentation.controllers.order_detail_controller import OrderDetailController
from src.modules.orders.presentation.controllers.order_list_create_controller import OrderListCreateController

app_name = "orders"

urlpatterns: list[URLPattern] = [
    path("orders", OrderListCreateController.as_view(), name="order-list-create"),
    path("orders/<uuid:order_id>", OrderDetailController.as_view(), name="order-detail"),
]
