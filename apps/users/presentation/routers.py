from django.urls import path

from apps.users.presentation.controllers.auth_controler import (
    LoginController,
    LogoutController,
    RefreshController,
    RegisterController,
    TokenVerifyController,
)
from apps.users.presentation.controllers.user_controler import (
    UserDetailController,
    UserListCreateController,
)

app_name = "users"

urlpatterns: list = [
    # Users
    path(
        "users",
        UserListCreateController.as_view(),
        name="user-list-create",
    ),
    path(
        "users/<uuid:user_id>",
        UserDetailController.as_view(),
        name="user-detail",
    ),
    # Auth
    path(
        "auth/register",
        RegisterController.as_view(),
        name="register",
    ),
    path(
        "auth/login",
        LoginController.as_view(),
        name="login",
    ),
    path(
        "auth/refresh",
        RefreshController.as_view(),
        name="refresh",
    ),
    path(
        "auth/verify",
        TokenVerifyController.as_view(),
        name="verify",
    ),
    path(
        "auth/logout",
        LogoutController.as_view(),
        name="logout",
    ),
    # TODO: Pending implementation
    # "auth/me",
    # "auth/password/change",
    # "auth/password/reset",
    # "auth/password/reset/confirm",
]
