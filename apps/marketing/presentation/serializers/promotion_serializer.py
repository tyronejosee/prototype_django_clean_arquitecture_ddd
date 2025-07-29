from rest_framework import serializers


class PromotionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    discount_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_active = serializers.BooleanField()
