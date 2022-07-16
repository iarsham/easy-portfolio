from django.urls import path
from dj_rest_auth.registration.views import RegisterView, LoginView
from dj_rest_auth.views import LogoutView, PasswordChangeView
from .views import UserDetailApiView, RevokeApiKeyView

app_name = 'api'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('user/', UserDetailApiView.as_view(), name='user_detail'),
    path('user/update/', UserDetailApiView.as_view(), name='user_update'),
    path('user/delete/', UserDetailApiView.as_view(), name='user_delete'),
    path('revoke_key/', RevokeApiKeyView.as_view(), name='revoke_key'),
]
