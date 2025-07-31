from modules.users.domain.exceptions import LogoutError
from modules.users.domain.interfaces.token_service_interface import (
    TokenServiceInterface,
)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class TokenService(TokenServiceInterface):
    # Messages
    INVALID_TOKEN_MSG: str = "Invalid or expired token"

    def blacklist(self, refresh_token: str) -> None:
        try:
            token = RefreshToken(refresh_token)  # type: ignore[arg-type]
            token.blacklist()
        except TokenError as error:
            raise LogoutError(self.INVALID_TOKEN_MSG) from error
