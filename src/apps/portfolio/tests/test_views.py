from django.urls import reverse
from django.test.client import MULTIPART_CONTENT, encode_multipart
from rest_framework import status
from apps.extensions.test_setup import PortfolioApiTestCase
from apps.extensions.utils import create_test_image
from apps.portfolio.models import Skill


class PortfolioViewsApiTest(PortfolioApiTestCase):

    def test_retrieve_about_me_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(viewname='portfolio:about_me')
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_aboutme_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        payload = {
            'first_name': 'james',
            'last_name': 'rodriguez',
        }
        path = reverse(viewname='portfolio:about_me')
        response = self.client.put(path=path, data=payload)
        self.assertNotEqual(response.data['first_name'], None)

    def test_update_aboutme_multipart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(viewname='portfolio:about_me')
        image_objects = [create_test_image() for _ in range(3)]
        payload = {
            'first_name': 'james',
            'file': image_objects
        }
        content = encode_multipart('BoUnDaRyStRiNg', payload)
        response = self.client.put(
            path=path, data=content, content_type=MULTIPART_CONTENT
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.aboutme2.aboutme_profile.count(), 3)

    def test_delete_aboutme_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(
            viewname='portfolio:aboutme_delete_profile',
            args=[self.aboutme_profile.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(
            viewname='portfolio:aboutme_delete_profile',
            args=[self.aboutme_profile.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_education_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        path = reverse(viewname='portfolio:education')
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['institute'], None)

    def test_update_education_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        payload = {
            'institute': 'Harvard University',
            'field_study': 'IT Computer',
            'degree': 'A+',
            'start_time': '2016-01-02',
        }
        path = reverse(viewname='portfolio:education')
        response = self.client.put(path=path, data=payload)
        self.assertEqual(response.data['institute'], 'Harvard University')
        self.assertNotEqual(response.data['degree'], None)

    def test_retrieve_skill_status_code_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(viewname='portfolio:skill-list')
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(self.aboutme.about_skill.all(), [self.skill])

    def test_create_skill(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(viewname='portfolio:skill-list')
        response = self.client.post(path=path, data={'name': 'c++'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'c++')

    def test_update_skill_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(viewname='portfolio:skill-detail', args=[self.skill.pk])
        response = self.client.put(path=path, data={'name': 'golang'})
        self.assertNotEqual(response.data['name'], self.skill.name)
        self.assertEqual(response.data['name'], 'golang')

    def test_delete_skill(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(viewname='portfolio:skill-detail', args=[self.skill.pk])
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Skill.objects.all().count(), 0)

    def test_delete_skill_certificate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        path = reverse(
            viewname='portfolio:skill_delete_certificate',
            args=[self.skill_certificate.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(
            viewname='portfolio:skill_delete_certificate',
            args=[self.skill_certificate.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_language_status_code_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(viewname='portfolio:language-list')
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(self.aboutme2.about_language.all(), [self.language])

    def test_create_language(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        path = reverse(viewname='portfolio:language-list')
        payload = {
            'name': 'dutch',
            'proficiency': 'professional-working',
        }
        response = self.client.post(path=path, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['proficiency'], 'professional-working')

    def test_update_language_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(
            viewname='portfolio:language-detail',
            args=[self.language.pk]
        )
        payload = {
            'name': 'persian',
            'proficiency': 'native-or-bilingual',
        }
        response = self.client.put(path=path, data=payload)
        self.assertNotEqual(response.data['name'], self.language.name)
        self.assertEqual(response.data['name'], 'persian')

    def test_delete_language_404(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(
            viewname='portfolio:language-detail',
            args=[self.language.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_language_certificate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(
            viewname='portfolio:language_delete_certificate',
            args=[self.language_certificate.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(
            viewname='portfolio:language_delete_certificate',
            args=[self.language_certificate.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_achievement_status_code_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        path = reverse(viewname='portfolio:achievement-list')
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(self.aboutme3.about_achieve.all(), [self.achievement])

    def test_create_achievement(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(viewname='portfolio:achievement-list')
        payload = {
            'title': 'new title',
            'description': 'new description',
        }
        response = self.client.post(path=path, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'new title')

    def test_update_achievement(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        path = reverse(
            viewname='portfolio:achievement-detail',
            args=[self.achievement.pk]
        )
        payload = {
            'title': 'edited title',
            'description': 'edited description',
        }
        response = self.client.put(path=path, data=payload)
        self.assertNotEqual(response.data['title'], self.achievement.title)
        self.assertEqual(response.data['description'], 'edited description')

    def test_delete_achievement(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        path = reverse(
            viewname='portfolio:achievement-detail',
            args=[self.achievement.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_achievement_certificate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(
            viewname='portfolio:achievement_delete_certificate',
            args=[self.achievement_certificate.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        path = reverse(
            viewname='portfolio:achievement_delete_certificate',
            args=[self.achievement_certificate.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
