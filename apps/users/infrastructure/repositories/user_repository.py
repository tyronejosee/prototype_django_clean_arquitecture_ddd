from uuid import UUID

from django.db.models import Q

from apps.users.domain.entities.user import User
from apps.users.domain.factories.user_factory import UserFactory
from apps.users.domain.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from apps.users.infrastructure.models.user_model import UserModel


class UserRepository(UserRepositoryInterface):
    def get_by_id(self, user_id: UUID) -> User | None:
        try:
            user_model = UserModel.objects.get(pk=user_id, is_active=True)
            return UserFactory.from_model(user_model)
        except UserModel.DoesNotExist:
            return None

    def get_by_email_or_username(self, email: str, username: str) -> User | None:
        try:
            user_model: UserModel = UserModel.objects.get(
                Q(email=email) | Q(username=username),
                is_active=True,
            )
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
            username=user.username,
            password=user.password,
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
