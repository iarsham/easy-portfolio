from django.urls import path
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView, LoginView
from dj_rest_auth.views import LogoutView, PasswordChangeView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from dj_rest_auth.registration.views import (
    VerifyEmailView, ResendEmailVerificationView
)
from apps.users.api.views import (
    GithubLoginApiView, GoogleLoginApiView
)

app_name = "config"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'login/google/',
        GoogleLoginApiView.as_view(),
        name='login_google'
    ),
    path(
        'login/github/',
        GithubLoginApiView.as_view(),
        name='login_github'
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'resend_verification_email/',
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email"
    ),
    path(
        'email_verification_sent/',
        ConfirmEmailView.as_view(),
        name='account_email_verification_sent'
    ),
    path(
        'confirm-email/<str:key>/',
        VerifyEmailView.as_view(),
        name='account_confirm_email'
    ),
]
