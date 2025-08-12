from typing import Any

import pytest
from django.contrib.auth.hashers import identify_hasher

from src.modules.users.infrastructure.services.password_service import PasswordService

password_service = PasswordService()


class TestPasswordService:
    def test_hash_and_verify_password(self) -> None:
        raw = "mysecretpassword"
        hashed = password_service.hash_password(raw)

        assert hashed != raw
        assert password_service.verify_password(raw, hashed) is True
        assert password_service.verify_password("wrongpass", hashed) is False

        identify_hasher(hashed)

    def test_verify_unusable_password_returns_false(self) -> None:
        unusable = password_service.hash_password(None)
        assert password_service.verify_password("any", unusable) is False

    @pytest.mark.parametrize("bad_input", [123, 12.5, [], {}, object()])
    def test_hash_password_type_error(self, bad_input: Any) -> None:
        with pytest.raises(TypeError):
            password_service.hash_password(bad_input)

    @pytest.mark.parametrize("bad_input", [123, 12.5, [], {}, object()])
    def test_verify_password_returns_false_for_invalid_inputs(self, bad_input: Any) -> None:
        assert password_service.verify_password(bad_input, "somehash") is False
        assert password_service.verify_password("raw", bad_input) is False
