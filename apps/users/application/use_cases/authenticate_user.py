from ...domain.entities.user import User
from ...domain.interfaces.repositories import UserRepositoryInterface
from ...domain.interfaces.services import PasswordServiceInterface


class AuthenticateUserUseCase:
    def __init__(
        self,
        repo: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
    ) -> None:
        self.repo = repo
        self.password_service = password_service

    def execute(self, email: str, password: str) -> User | None:
        user = self.repo.get_by_email(email)
        if user and self.password_service.verify_password(password, user.password):
            return user
        return None
