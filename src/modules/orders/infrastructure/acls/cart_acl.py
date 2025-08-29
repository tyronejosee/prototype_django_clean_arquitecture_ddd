from typing import override
from uuid import UUID

from src.modules.cart.infrastructure.models.cart_model import CartModel
from src.modules.orders.domain.contracts.cart_dtos import CartDTO, CartItemDTO
from src.modules.orders.domain.contracts.cart_service_interface import CartServiceInterface


class CartACL(CartServiceInterface):
    @override
    def get_cart(self, user_id: UUID) -> CartDTO | None:
        cart_model = CartModel.objects.filter(user_id=user_id).order_by("-updated_at").first()
        if not cart_model or cart_model.items.count() == 0:
            return None

        return CartDTO(
            id=cart_model.id,
            user_id=cart_model.user_id,
            items=[
                CartItemDTO(
                    id=item.id,
                    cart_id=cart_model.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in cart_model.items.all()
            ],
            created_at=cart_model.created_at,
            updated_at=cart_model.updated_at,
        )

    @override
    def clear_cart(self, user_id: UUID) -> None:
        cart_model = CartModel.objects.get(user_id=user_id)
        cart_model.items.all().delete()
