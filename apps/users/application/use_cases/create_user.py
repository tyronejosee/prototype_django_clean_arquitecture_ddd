from ...domain.entities.user import User
from ...domain.exceptions import UserAlreadyExistsException
from ...domain.factories.user import UserFactory
from ...domain.interfaces.repositories import UserRepositoryInterface
from ...domain.interfaces.services import PasswordServiceInterface


class CreateUserUseCase:
    def __init__(
        self,
        repo: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
    ) -> None:
        self.repo = repo
        self.password_service = password_service

    def execute(self, user_data: dict) -> User:
        if self.repo.get_by_email(user_data["email"]):
            raise UserAlreadyExistsException("User with this email already exists.")

        user_data["password"] = self.password_service.hash_password(
            user_data["password"]
        )
        user = UserFactory.from_dict(user_data)
        self.repo.create(user)
        return user  # TODO: Change to factory for User Created
