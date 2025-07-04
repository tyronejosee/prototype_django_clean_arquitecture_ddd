from apps.users.domain.entities.user import User
from apps.users.domain.exceptions import UserAlreadyExistsError
from apps.users.domain.factories.user import UserFactory
from apps.users.domain.interfaces.repositories import UserRepositoryInterface
from apps.users.domain.interfaces.services import PasswordServiceInterface


class CreateUserUseCase:
    def __init__(
        self,
        repo: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
    ) -> None:
        self.repo = repo
        self.password_service = password_service

    def execute(self, user_data: dict) -> User | None:
        if self.repo.get_by_email_or_username(
            user_data["email"],
            user_data["username"],
        ):
            raise UserAlreadyExistsError("Email or username already exists.")

        user_data["password"] = self.password_service.hash_password(
            user_data["password"],
        )
        user = UserFactory.from_dict(user_data)
        return self.repo.create(user)
