from uuid import UUID

from src.modules.users.domain.exceptions import UserDomainError, UserNotFoundError
from src.modules.users.domain.interfaces.password_service_interface import PasswordServiceInterface
from src.modules.users.domain.interfaces.user_repository_interface import UserRepositoryInterface


class ChangePasswordUseCase:
    # Messages
    USER_NOT_FOUND_MSG: str = "User not found."
    INVALID_CURRENT_PASSWORD_MSG: str = "Current password is incorrect."
    NEW_PASSWORD_MUST_BE_DIFFERENT_MSG: str = "New password must be different from the current password."
    PASSWORD_CHANGED_MSG: str = "Password changed successfully."

    def __init__(self, repo: UserRepositoryInterface, password_service: PasswordServiceInterface) -> None:
        self.repo = repo
        self.password_service = password_service

    def execute(self, user_id: UUID, current_password: str, new_password: str) -> str:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(self.USER_NOT_FOUND_MSG)

        # Verify current password against the actual stored password hash
        if not self.password_service.verify_password(current_password, user.password):
            raise UserDomainError(self.INVALID_CURRENT_PASSWORD_MSG)

        # Ensure new password is different from current password
        if self.password_service.verify_password(new_password, user.password):
            raise UserDomainError(self.NEW_PASSWORD_MUST_BE_DIFFERENT_MSG)

        # Hash new password and update user
        new_hashed_password = self.password_service.hash_password(new_password)
        user.password = new_hashed_password

        updated_user = self.repo.update(user_id, user)
        if not updated_user:
            raise UserNotFoundError(self.USER_NOT_FOUND_MSG)

        return self.PASSWORD_CHANGED_MSG
