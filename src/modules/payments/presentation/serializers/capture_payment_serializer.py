from rest_framework import serializers


class CapturePaymentSerializer(serializers.Serializer):
    external_id = serializers.CharField()
