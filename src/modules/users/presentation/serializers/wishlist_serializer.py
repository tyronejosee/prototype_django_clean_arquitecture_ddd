from rest_framework import serializers


class WishlistListSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    product_id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class WishlistCreateSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(required=True)
