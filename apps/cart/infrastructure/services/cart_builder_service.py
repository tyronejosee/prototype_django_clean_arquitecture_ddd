from apps.cart.domain.entities.cart import Cart
from apps.cart.infrastructure.models import CartItemModel, CartModel


class CartBuilderService:
    @staticmethod
    def update_cart(cart_model: CartModel, new_cart: Cart) -> None:
        current_items = {item.product_id: item for item in cart_model.items.all()}
        incoming_items = {item.product_id: item for item in new_cart.items}

        # Create or update items
        for product_id, new_item in incoming_items.items():
            if product_id in current_items:
                item_model = current_items[product_id]
                item_model.quantity = new_item.quantity.value
                item_model.unit_price = new_item.unit_price
                item_model.save()
            else:
                CartItemModel.objects.create(
                    cart=cart_model,
                    id=new_item.id,
                    product_id=new_item.product_id,
                    quantity=new_item.quantity.value,
                    unit_price=new_item.unit_price,
                )

        # Delete items
        to_delete = set(current_items) - set(incoming_items)
        if to_delete:
            CartItemModel.objects.filter(
                cart=cart_model,
                product_id__in=to_delete,
            ).delete()
