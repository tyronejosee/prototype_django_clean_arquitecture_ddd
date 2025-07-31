from django.contrib.auth.hashers import check_password, make_password
from django.utils.crypto import get_random_string

from src.modules.users.domain.interfaces.password_service_interface import (
    PasswordServiceInterface,
)


class PasswordService(PasswordServiceInterface):
    # Constants
    UNUSABLE_CREDENTIAL_PREFIX = "!"
    UNUSABLE_CREDENTIAL_SUFFIX_LENGTH = 40

    # Messages
    TYPE_ERROR_MSG = "Password must be str or bytes"

    def hash_password(self, raw_password: str | None) -> str:
        if raw_password is None:
            return self.UNUSABLE_CREDENTIAL_PREFIX + get_random_string(
                self.UNUSABLE_CREDENTIAL_SUFFIX_LENGTH,
            )
        if not isinstance(raw_password, str | bytes):
            raise TypeError(self.TYPE_ERROR_MSG)
        return make_password(raw_password)

    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        if not isinstance(raw_password, str | bytes):
            return False
        if not isinstance(hashed_password, str | bytes):
            return False
        if hashed_password.startswith(self.UNUSABLE_CREDENTIAL_PREFIX):
            return False
        return check_password(raw_password, hashed_password)
