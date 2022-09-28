from django.urls import reverse
from rest_framework import status
from apps.extensions.test_setup import PortfolioApiTestCase
from apps.portfolio.api.serializers import AboutMeSerializer, EducationSerializer


class SerializerPortfolioApiTest(PortfolioApiTestCase):

    def test_aboutme_data(self):
        serializer = AboutMeSerializer(
            instance=self.aboutme3,
            context={'request': self.client.request()}
        )
        self.assertEqual(serializer.data['profile_images'], [])

    def test_validate_education_datetime(self):
        invalid_data = {
            'start_time': '2021-06-07',
            'finish_time': '2019-01-07',
        }
        serializer = EducationSerializer(
            instance=self.aboutme2.about_education,
            data=invalid_data,
        )
        serializer.is_valid()
        self.assertTrue(status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            serializer.errors['non_field_errors'][0],
            'The end date cannot be less than the start date'
        )

    def test_education_to_representation_method(self):
        payload = {
            'start_time': '2021-06-07',
            'finish_time': '2022-01-07',
        }
        serializer = EducationSerializer(
            instance=self.aboutme3.about_education,
            data=payload,
        )
        serializer.is_valid(), serializer.save()
        self.assertEqual(serializer.data['status'], 'finished')
        payload['finish_time'] = None
        serializer = EducationSerializer(
            instance=self.aboutme3.about_education,
            data=payload,
        )
        serializer.is_valid(), serializer.save()
        self.assertEqual(serializer.data['status'], 'until now')

    def test_validate_create_skill(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        response = self.client.post(
            path=reverse("portfolio:skill-list"),
            data={'name': 'python'},
        )
        expected_response = "This skill already exists"
        self.assertTrue(status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0], expected_response)

    def test_validate_create_language(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        response = self.client.post(
            path=reverse("portfolio:language-list"),
            data={'name': 'Germany', 'proficiency': 'elementary', }
        )
        expected_response = "This language already exists"
        self.assertTrue(status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0], expected_response)

    def test_validate_create_achievement(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        response = self.client.post(
            path=reverse("portfolio:achievement-list"),
            data={
                'title': self.achievement.title,
                'description': self.achievement.description
            }
        )
        expected_response = "This achievement already exists"
        self.assertTrue(status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['title'][0], expected_response)
