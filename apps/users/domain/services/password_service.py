"""Services for the users domain"""

import bcrypt
import secrets
import string

from ..exceptions import UserDomainException
from ..interfaces.services import PasswordServiceInterface


UNUSABLE_PASSWORD_PREFIX = "!"
UNUSABLE_PASSWORD_PREFIX_BYTES = b"!"
UNUSABLE_PASSWORD_SUFFIX_LENGTH = 40


class PasswordService(PasswordServiceInterface):
    @staticmethod
    def _generate_unusable_password() -> str:
        suffix = "".join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(UNUSABLE_PASSWORD_SUFFIX_LENGTH)
        )
        return UNUSABLE_PASSWORD_PREFIX + suffix

    @staticmethod
    def hash_password(raw_password: str | None) -> str:
        """
        Hashes a password using bcrypt.
        If `raw_password` is None generates an unusable password hash.
        """
        if raw_password is None:
            return PasswordService._generate_unusable_password()

        if not isinstance(raw_password, (str, bytes)):
            raise UserDomainException(
                "Password must be a string or bytes, "
                f"got {type(raw_password).__qualname__}"
            )

        password_bytes: bytes = (
            raw_password.encode("utf-8")
            if isinstance(raw_password, str)
            else raw_password
        )

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(raw_password: str, hashed_password: str) -> bool:
        """
        Verifies a raw password against the stored bcrypt hash.
        If the password is unusable, returns False.
        """
        if not isinstance(raw_password, (str, bytes)):
            raise UserDomainException(
                "Password must be a string or bytes, "
                f"got {type(raw_password).__qualname__}"
            )

        if not isinstance(hashed_password, (str, bytes)):
            raise UserDomainException(
                "Hashed password must be a string or bytes, "
                f"got {type(hashed_password).__qualname__}"
            )

        raw_bytes: bytes = (
            raw_password.encode("utf-8")
            if isinstance(raw_password, str)
            else raw_password
        )

        hashed_bytes: bytes = (
            hashed_password.encode("utf-8")
            if isinstance(hashed_password, str)
            else hashed_password
        )

        # Prevent attempts to verify against unusable password
        if hashed_bytes.startswith(UNUSABLE_PASSWORD_PREFIX_BYTES):
            return False

        return bcrypt.checkpw(raw_bytes, hashed_bytes)
