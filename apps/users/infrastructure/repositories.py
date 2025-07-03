from uuid import UUID

from .models import UserModel
from ..domain.entities.user import User
from ..domain.factories.user import UserFactory
from ..domain.interfaces.repositories import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    def get_by_id(self, user_id: UUID) -> User | None:
        try:
            user_model = UserModel.objects.get(pk=user_id, is_active=True)
            return UserFactory.from_model(user_model)
        except UserModel.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> User | None:
        try:
            user_model = UserModel.objects.get(email=email, is_active=True)
            return UserFactory.from_model(user_model)
        except UserModel.DoesNotExist:
            return None

    def list_all(self) -> list[User]:
        return [
            UserFactory.from_model(user_model)
            for user_model in UserModel.objects.filter(is_active=True)
        ]

    def create(self, user: User) -> User:
        user_model = UserModel.objects.create(
            email=user.email,
            password=user.password,  # This expects a hashed password
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
        )
        return UserFactory.from_model(user_model)

    def update(self, user_id: UUID, user: User) -> User | None:
        updated = UserModel.objects.filter(pk=user_id).update(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
        )
        if updated:
            user_model = UserModel.objects.get(pk=user_id)
            return UserFactory.from_model(user_model)
        return None

    def delete(self, user_id: UUID) -> None:
        try:
            user_model = UserModel.objects.get(pk=user_id)
            user_model.is_active = False
            user_model.save()
        except UserModel.DoesNotExist:
            pass
