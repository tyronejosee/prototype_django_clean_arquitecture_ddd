from rest_framework import serializers


class CartItemSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class CartItemCreateSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True, required=True)


class CartItemPatchSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class CartSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(required=False, allow_null=True)
    items = CartItemSerializer(many=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
