from apps.users.domain.interfaces.token_service_interface import TokenServiceInterface


class LogoutUserUseCase:
    def __init__(self, token_service: TokenServiceInterface) -> None:
        self.token_service = token_service

    def execute(self, refresh_token: str) -> None:
        self.token_service.blacklist(refresh_token)
