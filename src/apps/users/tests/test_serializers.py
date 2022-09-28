from rest_framework import status
from apps.extensions.test_setup import GeneralApiTestCase
from apps.users.api.serializers import (
    UserDetailSerializer, UserUpdateSerializer
)


class UserSerializerApiTest(GeneralApiTestCase):

    def test_user_detail_serializer_data(self):
        serializer = UserDetailSerializer(instance=self.user3)
        self.assertEqual(serializer.data['verify'], True)

    def test_user_update_data(self):
        payload = {'username': 'new_username'}
        serializer = UserUpdateSerializer(instance=self.user3, data=payload)
        serializer.is_valid(), serializer.save()
        self.assertEqual(serializer.data['username'], 'new_username')

    def test_validate_unique_data(self):
        payload = {
            'email': 'username3@email.com',
            'username': 'username3',
        }
        serializer = UserUpdateSerializer(instance=self.user2, data=payload)
        serializer.is_valid()
        expected_validate = 'A user with that username already exists.'
        self.assertTrue(status.HTTP_400_BAD_REQUEST)
        self.assertEqual(serializer.errors['username'][0], expected_validate)
