from rest_framework import serializers


class CapturePaymentSerializer(serializers.Serializer):
    paypal_order_id = serializers.CharField()
