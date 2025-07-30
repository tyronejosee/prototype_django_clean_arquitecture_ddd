from rest_framework import serializers


class PromotionSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    discount_percent = serializers.DecimalField(max_digits=5, decimal_places=2)
    is_active = serializers.BooleanField()
    starts_at = serializers.DateTimeField()
    ends_at = serializers.DateTimeField()
