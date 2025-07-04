from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string

from apps.users.domain.interfaces.services import PasswordServiceInterface

UNUSABLE_PASSWORD_PREFIX = "!"
UNUSABLE_PASSWORD_SUFFIX_LENGTH = 40


class PasswordService(PasswordServiceInterface):
    def hash_password(self, raw_password: str | None) -> str:
        if raw_password is None:
            return UNUSABLE_PASSWORD_PREFIX + get_random_string(
                UNUSABLE_PASSWORD_SUFFIX_LENGTH
            )
        if not isinstance(raw_password, (str, bytes)):
            raise TypeError("Password must be str or bytes")
        return make_password(raw_password)

    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        if not isinstance(raw_password, (str, bytes)):
            return False
        if not isinstance(hashed_password, (str, bytes)):
            return False
        if hashed_password.startswith(UNUSABLE_PASSWORD_PREFIX):
            return False
        return check_password(raw_password, hashed_password)
