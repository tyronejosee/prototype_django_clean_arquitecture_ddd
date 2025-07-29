from rest_framework import serializers

from .order_item_serializer import OrderItemSerializer


class OrderSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    status = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    final_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )
    applied_discounts = serializers.ListField(read_only=True)
    coupon = serializers.DictField(read_only=True)
    promotions = serializers.ListField(read_only=True)

    def get_status(self, obj) -> str:
        return obj.status.value if hasattr(obj.status, "value") else str(obj.status)
