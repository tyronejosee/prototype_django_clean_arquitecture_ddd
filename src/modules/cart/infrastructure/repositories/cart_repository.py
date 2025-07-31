from decimal import Decimal
from typing import override
from uuid import UUID

from modules.cart.domain.entities.cart import Cart
from modules.cart.domain.exceptions import (
    CartDomainError,
    CartItemNotFoundError,
    CartNotFoundError,
)
from modules.cart.domain.factories.cart_factory import CartFactory
from modules.cart.domain.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)
from modules.cart.infrastructure.models.cart_item_model import CartItemModel
from modules.cart.infrastructure.models.cart_model import CartModel
from modules.cart.infrastructure.services.cart_builder_service import CartBuilderService


class CartRepository(CartRepositoryInterface):
    # Messages
    CART_NOT_FOUND_MSG: str = "Cart not found."
    CART_ALREADY_EXISTS_MSG: str = "Cart already exists."
    ITEM_NOT_FOUND_MSG: str = "Item not found."

    @override
    def get_by_user(self, user_id: UUID) -> Cart:
        cart_model = CartModel.objects.filter(user_id=user_id).order_by("-updated_at").first()
        if cart_model is None:
            raise CartNotFoundError(self.CART_NOT_FOUND_MSG)
        return CartFactory.from_model(cart_model)

    @override
    def create(self, cart: Cart) -> Cart:
        if CartModel.objects.filter(user_id=cart.user_id).exists():
            raise CartDomainError(self.CART_ALREADY_EXISTS_MSG)

        cart_model = CartModel.objects.create(
            id=cart.id,
            user_id=cart.user_id,
        )

        for item in cart.items:
            CartItemModel.objects.create(
                id=item.id,
                cart=cart_model,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        return CartFactory.from_model(cart_model)

    @override
    def update(self, cart: Cart) -> Cart:
        try:
            cart_model = CartModel.objects.get(user_id=cart.user_id)
        except CartModel.DoesNotExist as err:
            raise CartNotFoundError(self.CART_NOT_FOUND_MSG) from err

        CartBuilderService.update_cart(cart_model, cart)
        return self.get_by_user(cart.user_id)

    @override
    def patch_item(self, user_id: UUID, item_id: UUID, quantity: int) -> Cart:
        try:
            item = CartItemModel.objects.get(id=item_id)
            item.quantity = quantity
            item.save()
        except CartItemModel.DoesNotExist as err:
            raise CartItemNotFoundError(self.ITEM_NOT_FOUND_MSG) from err
        return self.get_by_user(user_id=user_id)

    @override
    def delete_item(self, user_id: UUID, item_id: UUID) -> Cart:
        cart_item = CartItemModel.objects.filter(id=item_id)
        if not cart_item:
            raise CartItemNotFoundError(self.ITEM_NOT_FOUND_MSG)
        cart_item.delete()
        return self.get_by_user(user_id=user_id)

    @override
    def preview(self, cart: Cart) -> dict:
        # ! TODO: Implement preview logic and service
        tax = Decimal(0.19)
        total = cart.total()
        taxes = total * tax
        grand_total = total + taxes
        return {
            "subtotal": total,
            "taxes": taxes,
            "total": grand_total,
        }

    @override
    def clear(self, user_id: UUID) -> None:
        try:
            cart_model = CartModel.objects.get(user_id=user_id)
            cart_model.items.all().delete()  # type: ignore[union-attr]
        except CartModel.DoesNotExist as err:
            raise CartNotFoundError(self.CART_NOT_FOUND_MSG) from err
