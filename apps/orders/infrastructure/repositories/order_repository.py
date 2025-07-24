from typing import override
from uuid import UUID

from apps.orders.domain.entities.order import Order
from apps.orders.domain.exceptions import OrderNotFoundError
from apps.orders.domain.factories.order_factory import OrderFactory
from apps.orders.domain.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)
from apps.orders.domain.value_objects.order_status import OrderStatus
from apps.orders.infrastructure.models import OrderItemModel, OrderModel


class OrderRepository(OrderRepositoryInterface):
    # Messages
    ORDER_NOT_FOUND_MSG: str = "Order {order_id} not found."

    @override
    def create(self, order: Order) -> Order:
        order_model = OrderModel.objects.create(
            id=order.id,
            user_id=order.user_id,
            status=order.status.value,
        )

        for item in order.items:
            OrderItemModel.objects.create(
                id=item.id,
                order=order_model,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )

        return OrderFactory.from_model(order_model)

    @override
    def get_by_id(self, order_id: UUID) -> Order:
        try:
            model = OrderModel.objects.prefetch_related("items").get(id=order_id)
        except OrderModel.DoesNotExist as error:
            raise OrderNotFoundError(
                self.ORDER_NOT_FOUND_MSG.format(order_id=order_id),
            ) from error

        return OrderFactory.from_model(model)

    @override
    def list_by_user(self, user_id: UUID) -> list[Order]:
        queryset = OrderModel.objects.filter(user_id=user_id).prefetch_related("items")
        return [OrderFactory.from_model(order) for order in queryset]

    @override
    def update(self, order: Order) -> Order:
        try:
            model = OrderModel.objects.get(id=order.id)
        except OrderModel.DoesNotExist as error:
            raise OrderNotFoundError(
                self.ORDER_NOT_FOUND_MSG.format(order_id=order.id),
            ) from error
        model.status = order.status.value
        model.save()
        return self.get_by_id(order.id)

    @override
    def cancel(self, order_id: UUID) -> Order:
        model = OrderModel.objects.get(id=order_id)
        model.status = OrderStatus.CANCELLED.value
        model.save()
        return self.get_by_id(order_id)

    @override
    def update_status(self, order_id: UUID, status: str) -> None:
        model = OrderModel.objects.get(id=order_id)
        model.status = status
        model.save()
