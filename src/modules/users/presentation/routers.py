from django.urls import path

from src.modules.users.presentation.controllers.auth_controler import (
    ChangePasswordController,
    LoginController,
    LogoutController,
    RefreshController,
    RegisterController,
    TokenVerifyController,
)
from src.modules.users.presentation.controllers.user_controler import UserDetailController, UserListCreateController
from src.modules.users.presentation.controllers.wishlist_controller import WishlistController, WishlistDetailController

app_name = "users"

urlpatterns: list = [
    # Users
    path("users", UserListCreateController.as_view(), name="user-list-create"),
    path("users/<uuid:user_id>", UserDetailController.as_view(), name="user-detail"),
    # Auth
    path("auth/register", RegisterController.as_view(), name="register"),
    path("auth/login", LoginController.as_view(), name="login"),
    path("auth/refresh", RefreshController.as_view(), name="refresh"),
    path("auth/verify", TokenVerifyController.as_view(), name="verify"),
    path("auth/password/change", ChangePasswordController.as_view(), name="change-password"),
    path("auth/logout", LogoutController.as_view(), name="logout"),
    # Wishlist
    path("wishlist", WishlistController.as_view(), name="wishlist-list-create"),
    path("wishlist/<uuid:product_id>", WishlistDetailController.as_view(), name="wishlist-detail"),
    # TODO: Pending implementation
    # "auth/me",
    # "auth/password/reset",
    # "auth/password/reset/confirm",
]
