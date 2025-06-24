"""Serializers (DTOs) for the catalog interfaces."""

from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True)
    parent_id = serializers.UUIDField(required=False, allow_null=True)
    image_url = serializers.URLField(required=False, allow_null=True)
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class ProductSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    sku = serializers.CharField(max_length=100)
    category_id = serializers.UUIDField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    stock = serializers.IntegerField()
    min_stock = serializers.IntegerField()
    image_url = serializers.URLField(required=False, allow_null=True)
    is_active = serializers.BooleanField()
    is_featured = serializers.BooleanField()
    weight = serializers.DecimalField(
        max_digits=8, decimal_places=3, required=False, allow_null=True
    )
    unit = serializers.CharField(max_length=10)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
