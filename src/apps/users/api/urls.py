from django.urls import path
from dj_rest_auth.registration.views import RegisterView, LoginView
from dj_rest_auth.views import LogoutView, PasswordChangeView
from .views import (
    UserDetailApiView, RevokeApiKeyView,
    UserUpdateApiView, UserDeleteApiView,
    GoogleLoginApiView, GithubLoginApiView
)

app_name = 'api'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/google/', GoogleLoginApiView.as_view(), name='login_google'),
    path('login/github/', GithubLoginApiView.as_view(), name='login_github'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('user/', UserDetailApiView.as_view(), name='user_detail'),
    path('user/update/', UserUpdateApiView.as_view(), name='user_update'),
    path('user/delete/', UserDeleteApiView.as_view(), name='user_delete'),
    path('revoke_key/', RevokeApiKeyView.as_view(), name='revoke_key'),
]