from django.urls import path
from .views import (
    RegisterView,
    ActivateAccountView,
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    AdminRegisterView,
    UserListView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("admin/register/",AdminRegisterView.as_view(),name="admin-register"),
    path("activate/<str:uidb64>/<str:token>/", ActivateAccountView.as_view(), name="activate"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password-reset-confirm/<str:uidb64>/<str:token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('user/list/',UserListView.as_view(),name='user-list'),
]
