from django.urls import path
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView
from dj_rest_auth.registration.views import RegisterView
from apps.users.api.views import GithubLoginApiView, GoogleLoginApiView

app_name = "config"

urlpatterns = [
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
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
        'logout/',
        LogoutView.as_view(),
        name='rest_logout'
    ),
    path(
        'password/change/',
        PasswordChangeView.as_view(),
        name='rest_password_change'
    )
]
