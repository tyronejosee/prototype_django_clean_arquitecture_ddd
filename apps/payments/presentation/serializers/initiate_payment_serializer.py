from rest_framework import serializers


class InitiatePaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    payment_method = serializers.CharField()
    payment_data = serializers.JSONField()
