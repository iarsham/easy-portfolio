from django.urls import path
from apps.users.api.views import (
    UserGetPatchDeleteApiView, FetchApiKey
)

USER_ENDPOINTS = {
    "get": "retrieve_user",
    "put": "update_user",
    "delete": "delete_user",
}

app_name = 'users'

urlpatterns = [
    path(
        'user/',
        UserGetPatchDeleteApiView.as_view(USER_ENDPOINTS),
        name='user_rud'
    ),
    path('user/key/', FetchApiKey.as_view(), name='user_key')

]

