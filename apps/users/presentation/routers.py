from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.presentation.views import (
    UserDetailView,
    UserListCreateView,
    UserLoginView,
)

app_name = "users"

urlpatterns: list = [
    path(
        "users",
        UserListCreateView.as_view(),
        name="user-list",
    ),
    path(
        "users/<uuid:user_id>",
        UserDetailView.as_view(),
        name="user-detail",
    ),
    path(
        "auth/login",
        UserLoginView.as_view(),
        name="user-login",
    ),
    path(
        "auth/token",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
