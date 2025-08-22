import pytest

from src.modules.users.domain.exceptions import UserDomainError
from src.modules.users.domain.value_objects.email import Email
from src.modules.users.domain.value_objects.username import Username


class TestEmail:
    def test_valid_email_creates_successfully(self) -> None:
        # Given: a valid email address
        email_str = "user@example.com"

        # When: creating the Email value object
        email = Email(email_str)

        # Then: it should store the value correctly
        assert email.value == email_str
        assert str(email) == email_str

    @pytest.mark.parametrize(
        "invalid_email",
        [
            "plainaddress",
            "missingatsign.com",
            "missingdomain@.com",
            "missingdot@domaincom",
            "@missingusername.com",
            "",
            "   ",
        ],
    )
    def test_invalid_email_format_raises_error(self, invalid_email: str) -> None:
        # Given: invalid email strings including None
        # When & Then: creating Email should raise UserDomainError
        with pytest.raises(UserDomainError, match=Email.EMAIL_INVALID_FORMAT_MSG):
            Email(invalid_email)  # type: ignore


class TestUsername:
    def test_valid_username_creates_successfully(self) -> None:
        # Given: a valid username
        valid_username = "user_123.Name"

        # When: creating the Username value object
        username = Username(valid_username)

        # Then: it should store the value correctly
        assert username.value == valid_username
        assert str(username) == valid_username

    @pytest.mark.parametrize("invalid_username", [None, ""])
    def test_username_required_raises_error(self, invalid_username: str | None) -> None:
        # Given: a missing or empty username
        # When & Then: should raise UserDomainError with required message
        with pytest.raises(UserDomainError, match=Username.USERNAME_REQUIRED_MSG):
            Username(invalid_username)  # type: ignore

    @pytest.mark.parametrize("short_username", ["a", "ab", "abc"])
    def test_username_too_short_raises_error(self, short_username: str) -> None:
        # Given: username shorter than MIN_LENGTH (4)
        # When & Then: should raise UserDomainError with too short message
        with pytest.raises(UserDomainError, match=Username.USERNAME_TOO_SHORT_MSG):
            Username(short_username)

    @pytest.mark.parametrize(
        "long_username",
        ["a" * 31, "username_that_is_definitely_way_too_long_123456"],
    )
    def test_username_too_long_raises_error(self, long_username: str) -> None:
        # Given: username longer than MAX_LENGTH (30)
        # When & Then: should raise UserDomainError with too long message
        with pytest.raises(UserDomainError, match=Username.USERNAME_TOO_LONG_MSG):
            Username(long_username)

    @pytest.mark.parametrize(
        "invalid_format_username",
        ["user!", "user name", "user@name", "user#name", "user$name", "user,name"],
    )
    def test_username_invalid_format_raises_error(self, invalid_format_username: str) -> None:
        # Given: username with invalid characters
        # When & Then: should raise UserDomainError with invalid format message
        with pytest.raises(UserDomainError, match=Username.USERNAME_INVALID_FORMAT_MSG):
            Username(invalid_format_username)
