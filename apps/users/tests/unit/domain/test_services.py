import pytest
from typing import Any

from ....domain.services.password_service import (
    PasswordService,
    UNUSABLE_PASSWORD_PREFIX,
)
from ....domain.exceptions import UserDomainException


def test_generate_unusable_password_format() -> None:
    unusable = PasswordService.hash_password(None)
    assert unusable.startswith(UNUSABLE_PASSWORD_PREFIX)
    assert len(unusable) == 1 + 40  # prefix + suffix


def test_hash_and_verify_password() -> None:
    raw = "mysecretpassword"
    hashed = PasswordService.hash_password(raw)
    assert hashed != raw
    assert PasswordService.verify_password(raw, hashed) is True
    assert PasswordService.verify_password("wrongpass", hashed) is False


def test_verify_unusable_password_returns_false() -> None:
    unusable = PasswordService.hash_password(None)
    assert PasswordService.verify_password("any", unusable) is False


@pytest.mark.parametrize("bad_input", [123, 12.5, [], {}])
def test_hash_password_typeerror(bad_input: Any) -> None:
    with pytest.raises(UserDomainException) as exc_info:
        PasswordService.hash_password(bad_input)
    assert "Password must be a string or bytes" in str(exc_info.value)


@pytest.mark.parametrize("bad_input", [123, 12.5, [], {}])
def test_verify_password_typeerror(bad_input: Any) -> None:
    with pytest.raises(UserDomainException) as exc_info:
        PasswordService.verify_password(bad_input, "hashed")
    assert "Password must be a string or bytes" in str(exc_info.value)

    with pytest.raises(UserDomainException) as exc_info_2:
        PasswordService.verify_password("raw", bad_input)
    assert "Hashed password must be a string or bytes" in str(exc_info_2.value)
