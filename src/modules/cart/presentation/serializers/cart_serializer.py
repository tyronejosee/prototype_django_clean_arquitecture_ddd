from rest_framework import serializers


class QuantityInputSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, required=True)


class CartItemInputSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)


class CartItemOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    product_id = serializers.UUIDField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)


class CartInputSerializer(serializers.Serializer):
    items = CartItemInputSerializer(many=True, required=True)


class CartOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    items = CartItemOutputSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
