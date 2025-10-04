from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)
from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("verify-email/", views.VerifyEmailView.as_view(), name="verify-email"),
    path("me/", views.UserMeView.as_view(), name="me"),
    path("client-profile/", views.ClientProfileView.as_view(), name="client-profile"),
    path("serviceman-profile/", views.ServicemanProfileView.as_view(), name="serviceman-profile"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password-reset/", views.PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset-confirm/", views.PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]