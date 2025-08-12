from src.modules.users.domain.entities.user import User
from src.modules.users.domain.exceptions import UserAlreadyExistsError
from src.modules.users.domain.factories.user_factory import UserFactory
from src.modules.users.domain.interfaces.password_service_interface import PasswordServiceInterface
from src.modules.users.domain.interfaces.user_repository_interface import UserRepositoryInterface


class CreateUserUseCase:
    # Messages
    USER_ALREADY_EXISTS_MSG: str = "Email or username already exists."

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
            raise UserAlreadyExistsError(self.USER_ALREADY_EXISTS_MSG)

        user_data["password"] = self.password_service.hash_password(
            user_data["password"],
        )
        user = UserFactory.from_dict(user_data)
        return self.repo.create(user)
