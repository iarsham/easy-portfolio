from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.users.api.views import (
    UserGetPatchDeleteApiView as UserView, FetchApiKey
)


class UsersUrlsApiTest(SimpleTestCase):

    def test_user_urls(self):
        path = resolve("/api/v1/user/")
        views = {
            "get": "retrieve_user",
            "patch": "update_user",
            "delete": "delete_user",
        }
        self.assertEqual(path.func.__name__, UserView.as_view(views).__name__)

    def test_user_key_url(self):
        path = reverse("users:user_key")
        self.assertEqual(resolve(path).func.view_class, FetchApiKey)
