from django.urls import reverse
from rest_framework import status
from apps.extensions.inheritances import GerneralApiTestCase
from apps.users.api.serializers import UserDetailSerializer


class UsersViewApiTest(GerneralApiTestCase):

    def setUp(self):
        self.user_path = reverse('users:user_rud')
        super().setUp()

    def test_retrieve_user_status_code(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"api-key {self.token1}"
        )
        response = self.client.get(path=self.user_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_data(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"api-key {self.token1}"
        )
        serializer = UserDetailSerializer(instance=self.user1)
        response = self.client.get(path=self.user_path)
        self.assertEqual(response.data, serializer.data)

    def test_update_user_data(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"api-key {self.token2}"
        )
        user_data = {'username': 'updated_username'}
        response = self.client.put(path=self.user_path, data=user_data)
        self.assertNotEqual(response.data['username'], 'username1')

    def test_delete_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"api-key {self.token2}"
        )
        response = self.client.delete(path=self.user_path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_unauthorize(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(path=self.user_path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(
            HTTP_AUTHORIZATION="api-key wrongtoken123321!!!"
        )
        response = self.client.get(path=self.user_path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
