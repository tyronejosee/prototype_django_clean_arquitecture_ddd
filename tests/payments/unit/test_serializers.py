from decimal import Decimal
from typing import cast
from uuid import uuid4

from src.modules.payments.presentation.serializers.payment_serializer import (
    InitiatePaymentInputSerializer,
    DetailsOuputSerializer,
    InitiatePaymentOutputSerializer,
    CapturePaymentOutputSerializer,
)


class TestInitiatePaymentInputSerializer:
    def test_valid_data_returns_expected_fields(self) -> None:
        # Given: valid input payment data
        data = {
            "order_id": uuid4(),
            "payment_method": "credit_card",
        }

        # When: serializing the input
        serializer = InitiatePaymentInputSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)

        # Then: output should match input
        assert result["order_id"] == data["order_id"]
        assert result["payment_method"] == "credit_card"


class TestDetailsOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Given: valid output details data
        data = {
            "order_id": uuid4(),
            "amount": Decimal("150.75"),
        }

        # When: serializing the output
        serializer = DetailsOuputSerializer(instance=data)
        result = cast(dict, serializer.data)

        # Then: output should match input
        assert result["order_id"] == str(data["order_id"])
        assert Decimal(result["amount"]) == Decimal("150.75")


class TestInitiatePaymentOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Given: valid output initiate payment data
        details_data = {
            "order_id": uuid4(),
            "amount": Decimal("200.00"),
        }
        data = {
            "external_id": "PAY-123456",
            "status": "pending",
            "redirect_url": "https://payment.gateway/redirect",
            "details": details_data,
        }

        # When: serializing the output
        serializer = InitiatePaymentOutputSerializer(instance=data)
        result = cast(dict, serializer.data)

        # Then: output should match input
        assert result["external_id"] == "PAY-123456"
        assert result["status"] == "pending"
        assert result["redirect_url"] == "https://payment.gateway/redirect"
        assert result["details"]["order_id"] == str(details_data["order_id"])
        assert Decimal(result["details"]["amount"]) == Decimal("200.00")


class TestCapturePaymentOutputSerializer:
    def test_instance_serialization_returns_expected_fields(self) -> None:
        # Given: valid output capture payment data
        data = {
            "external_id": "PAY-654321",
            "status": "captured",
            "details": {"transaction_id": "TX-7890", "method": "credit_card"},
        }

        # When: serializing the output
        serializer = CapturePaymentOutputSerializer(instance=data)
        result = cast(dict, serializer.data)

        # Then: output should match input
        assert result["external_id"] == "PAY-654321"
        assert result["status"] == "captured"
        assert result["details"]["transaction_id"] == "TX-7890"
        assert result["details"]["method"] == "credit_card"
