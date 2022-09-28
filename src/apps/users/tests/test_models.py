from apps.extensions.test_setup import GeneralApiTestCase
from django.contrib.auth import get_user_model


class UserModelTest(GeneralApiTestCase):

    def test_user_str_method(self):
        str_user = f"{self.user2.email} | {self.user2.username}"
        self.assertEqual(self.user2.__str__(), str_user)

    def test_user_created_attribute(self):
        self.assertFalse(self.user3.created)

    def test_user_is_superuser(self):
        self.assertTrue(self.user1.is_superuser)

    def test_users_list_count(self):
        users = get_user_model().objects.all().count()
        self.assertEqual(users, 3)
