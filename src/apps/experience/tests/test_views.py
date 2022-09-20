import json
from django.urls import reverse
from django.test.client import MULTIPART_CONTENT, encode_multipart
from rest_framework import status
from apps.extensions.inheritances import GerneralApiTestCase
from apps.experience.models import Project, ReferencePeople
from apps.extensions.utils import create_test_image


class ExperienceViewsApiTest(GerneralApiTestCase):
    def setUp(self):
        super().setUp()
        self.experience = self.user1.experience_user.create(
            role="Python Backend Developer",
            Employment_type="full-time",
            company_name="Booking.com",
            start_date="2018-02-01",
            still_working=True
        )
        self.project = self.experience.experience_project.create(
            name="Portfolio Backend Api",
            description='an open source api project with Django & Drf',
            stacks=[{"stack1": "python", "stack2": "postgres"}]
        )
        self.reference = self.user2.reference_user.create(
            full_name='Guido van Rossum',
            email='Guido1987@email.com',
            linkedin='https://www.linkedin.com/in/guido-van-rossum-4a0756',
            recommendation='Lorem Ipsum is simply dummy text of the printing'
        )
        self.blog = self.user3.blog_user.create(
            title='Commit Like a Pro',
            description='Committing changes is one of the common things that',
            link='https://imsadra.me/commit-like-a-pro'
        )
        self.personal_project = self.user1.personal_user.create(
            name='RestApi-Blog',
            stacks=[{'stack1': 'python', 'stack2': 'django'}],
            description='Blog Project With Django and Drf',
        )

    def test_retrieve_experience_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(viewname='experience:experience-list')
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_experience_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        payload = {
            'role': "Python Backend Developer Edited",
            'Employment_type': 'full-time',
            'company_name': 'Booking.com',
            'start_date': '2018-02-01',
            'still_working': True
        }
        path = reverse(
            viewname='experience:experience-detail',
            args=[self.experience.pk]
        )
        response = self.client.put(path=path, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['role'], self.experience.role)

    def test_delete_experience(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(
            viewname='experience:experience-detail',
            args=[self.experience.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_project_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(
            viewname='experience:project_CR',
            args=[self.experience.slug]
        )
        response = self.client.get(path=path)
        all_projects = Project.objects.filter(experience=self.experience)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(all_projects.count(), 1)

    def test_update_project_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        payload = {
            'name': 'Portfolio Backend Api Edited!',
            'description': 'an open source api project with Django & Drf',
            'stacks': [{"stack1": "python", "stack2": "postgres"}]
        }
        path = reverse(
            viewname='experience:project_UD',
            args=[self.experience.slug, self.project.pk]
        )
        response = self.client.put(path=path, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['name'], self.project.name)

    def test_update_project_multipart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(
            viewname='experience:project_UD',
            args=[self.experience.slug, self.project.pk]
        )
        image_objects = [create_test_image() for _ in range(2)]
        payload = {
            'name': 'Portfolio Backend Api Edited!',
            'description': 'an open source api project with Django & Drf',
            'stacks': [{}],
            'file': image_objects
        }
        content = encode_multipart('BoUnDaRyStRiNg', payload)
        response = self.client.put(
            path=path, data=content, content_type=MULTIPART_CONTENT
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.project.assets_project.count(), 2)

    def test_delete_project(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(
            viewname='experience:project_UD',
            args=[self.experience.slug, self.project.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_reference_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(viewname='experience:reference-list')
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(ReferencePeople.objects.all(), [self.reference])

    def test_create_reference(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        path = reverse(viewname='experience:reference-list')
        payload = {
            'full_name': 'elon musk',
            'email': 'elon@teslamotors.com',
            'linkedin': 'https://www.linkedin.com/company/spacex/',
            'recommendation': 'Lorem Ipsum is simply dummy text of the printing'
        }
        response = self.client.post(path=path, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'elon@teslamotors.com')

    def test_update_skill_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(
            viewname='experience:reference-detail',
            args=[self.reference.pk]
        )
        payload = {
            'full_name': 'Guido van Rossum',
            'email': 'Guido1987@email.com',
            'linkedin': 'https://www.linkedin.com/in/guido-van-rossum-4a0756',
            'recommendation': 'edition'
        }
        response = self.client.put(path=path, data=payload)
        self.assertNotEqual(response.data['recommendation'], self.reference.recommendation)
        self.assertEqual(response.data['recommendation'], 'edition')

    def test_delete_reference(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(
            viewname='experience:reference-detail',
            args=[self.reference.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(
            viewname='experience:reference-detail',
            args=[self.reference.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_blog_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        path = reverse(viewname='experience:blog-list')
        response = self.client.get(path=path)
        content = json.loads(response.content)
        self.assertEqual(content['count'], 1)
        self.assertEqual(content['next'], None)

    def test_create_blog(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(viewname='experience:blog-list')
        payload = {
            'title': 'From Alex’s Family',
            'link': 'https://alex.blog/2019/02/27/from-alexs-family/',
            'description': 'Alex was with his family when he passed peacefully',
        }
        response = self.client.post(path=path, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'From Alex’s Family')

    def test_update_blog_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        path = reverse(
            viewname='experience:blog-detail',
            args=[self.blog.pk]
        )
        payload = {
            'title': 'Commit Like a Pro',
            'description': 'Committing changes is one of the common things',
            'link': 'https://imsadra.me/commit-like-a-pro/edited/'
        }
        response = self.client.put(path=path, data=payload)
        self.assertNotEqual(response.data['link'], self.blog.link)

    def test_delete_blog(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        path = reverse(
            viewname='experience:blog-detail',
            args=[self.blog.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_personal_project_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(viewname='experience:personal_project-list')
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])

    def test_create_personal_project(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(viewname='experience:personal_project-list')
        payload = {
            'name': 'django-system-shop',
            'stacks': [{'stack1': 'html', 'stack2': 'css'}],
            'description': 'Shopping Django Project',
        }
        response = self.client.post(path=path, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'django-system-shop')

    def test_update_personal_project_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        path = reverse(
            viewname='experience:personal_project-detail',
            args=[self.personal_project.pk]
        )
        payload = {
            'name': 'RestApi-Blog edited!',
            'stacks': [{'stack1': 'python', 'stack2': 'django'}],
            'description': 'Blog Project With Django and Drf',
        }
        response = self.client.put(path=path, data=payload)
        self.assertNotEqual(response.data['name'], self.personal_project.name)

    def test_delete_personal_project(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        path = reverse(
            viewname='experience:personal_project-detail',
            args=[self.personal_project.pk]
        )
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
