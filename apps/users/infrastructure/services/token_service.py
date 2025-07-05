from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.domain.exceptions import LogoutError
from apps.users.domain.interfaces.token_service_interface import TokenServiceInterface


class TokenService(TokenServiceInterface):
    # Messages
    INVALID_TOKEN_MSG: str = "Invalid or expired token"

    def blacklist(self, refresh_token: str) -> None:
        try:
            token = RefreshToken(refresh_token)  # type: ignore[arg-type]
            token.blacklist()
        except Exception:
            raise LogoutError(self.INVALID_TOKEN_MSG)
