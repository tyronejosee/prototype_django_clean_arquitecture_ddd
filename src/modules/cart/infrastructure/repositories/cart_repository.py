from typing import override
from uuid import UUID

from src.modules.cart.domain.entities.cart import Cart
from src.modules.cart.domain.entities.cart_item import CartItem
from src.modules.cart.domain.exceptions import CartDomainError, CartItemNotFoundError, CartNotFoundError
from src.modules.cart.domain.factories.cart_factory import CartFactory
from src.modules.cart.domain.interfaces.cart_repository_interface import CartRepositoryInterface
from src.modules.cart.infrastructure.models.cart_item_model import CartItemModel
from src.modules.cart.infrastructure.models.cart_model import CartModel
from src.modules.cart.infrastructure.services.cart_item_merge_service import CartItemMergerService


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
    def create(self, user_id: UUID) -> Cart:
        if CartModel.objects.filter(user_id=user_id).exists():
            raise CartDomainError(self.CART_ALREADY_EXISTS_MSG)

        cart_model = CartModel.objects.create(user_id=user_id)
        return CartFactory.from_model(cart_model)

    @override
    def add_items(self, user_id: UUID, items: list[CartItem]) -> Cart:
        cart_model, _ = CartModel.objects.get_or_create(user_id=user_id)
        CartItemMergerService.add_or_merge_items(cart_model, items)
        return self.get_by_user(user_id)

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
    def delete_item(self, user_id: UUID, item_id: UUID) -> None:
        cart_item = CartItemModel.objects.filter(id=item_id)
        if not cart_item:
            raise CartItemNotFoundError(self.ITEM_NOT_FOUND_MSG)
        cart_item.delete()

    @override
    def clear(self, user_id: UUID) -> None:
        try:
            cart_model = CartModel.objects.get(user_id=user_id)
            cart_model.items.all().delete()  # type: ignore[union-attr]
        except CartModel.DoesNotExist as err:
            raise CartNotFoundError(self.CART_NOT_FOUND_MSG) from err
