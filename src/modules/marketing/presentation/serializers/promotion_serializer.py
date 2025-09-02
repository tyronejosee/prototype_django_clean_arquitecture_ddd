from rest_framework import serializers


class PromotionInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    discount_percent = serializers.DecimalField(max_digits=5, decimal_places=2)
    is_active = serializers.BooleanField()
    starts_at = serializers.DateTimeField()
    ends_at = serializers.DateTimeField()


class PromotionOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    discount_percent = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)
    is_active = serializers.BooleanField(read_only=True)
    starts_at = serializers.DateTimeField(read_only=True)
    ends_at = serializers.DateTimeField(read_only=True)
