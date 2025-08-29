from src.modules.cart.domain.entities.cart_item import CartItem
from src.modules.cart.infrastructure.models import CartItemModel, CartModel


class CartItemMergerService:
    @staticmethod
    def add_or_merge_items(cart_model: CartModel, new_items: list[CartItem]) -> None:
        existing_items = {item.product_id: item for item in cart_model.items.all()}  # type: ignore[union-attr]

        to_create: list[CartItemModel] = []
        to_update: list[CartItemModel] = []

        for item in new_items:
            quantity = int(item.quantity)
            unit_price = item.unit_price
            product_id = item.product_id

            if product_id in existing_items:
                existing_item = existing_items[product_id]
                existing_item.quantity = quantity
                existing_item.unit_price = unit_price
                to_update.append(existing_item)
            else:
                to_create.append(
                    CartItemModel(
                        id=item.id,
                        cart_id=cart_model,
                        product_id=product_id,
                        quantity=quantity,
                        unit_price=unit_price,
                    )
                )

        # Insert new items
        if to_create:
            CartItemModel.objects.bulk_create(to_create)

        # Update existing items
        if to_update:
            CartItemModel.objects.bulk_update(to_update, ["quantity"])
