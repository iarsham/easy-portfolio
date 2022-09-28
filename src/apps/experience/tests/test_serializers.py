from django.urls import reverse
from rest_framework import status
from apps.extensions.test_setup import ExperienceApiTestCase
from apps.experience.api.serializers import ExperienceSerializer


class ExperienceSerializerApiTest(ExperienceApiTestCase):

    def test_validate_experience_date(self):
        invalid_data = {
            'role': 'Python Backend Developer',
            'employment_type': 'full-time',
            'company_name': 'Booking.com',
            'start_date': '2018-02-01',
            'still_working': False
        }
        serializer = ExperienceSerializer(
            instance=self.experience,
            data=invalid_data
        )
        serializer.is_valid()
        validate_txt = 'Your work experience has ended. Enter the end date'
        self.assertTrue(status.HTTP_400_BAD_REQUEST)
        self.assertEqual(serializer.errors['non_field_errors'][0], validate_txt)

    def test_validate_experience_date2(self):
        invalid_data = {
            'role': 'Python Backend Developer',
            'employment_type': 'full-time',
            'company_name': 'Booking.com',
            'start_date': '2018-02-01',
            'still_working': True,
            'end_date': '2019-02-01',
        }
        serializer = ExperienceSerializer(
            instance=self.experience,
            data=invalid_data
        )
        serializer.is_valid()
        validate_txt = 'Your working now, dont need to end_date'
        self.assertTrue(status.HTTP_400_BAD_REQUEST)
        self.assertEqual(serializer.errors['non_field_errors'][0], validate_txt)

    def test_work_estimate_time(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        response = self.client.post(
            path=reverse("experience:experience-list"),
            data={
                'role': 'Golang Backend Developer',
                'employment_type': 'part-time',
                'company_name': 'Booking.com',
                'start_date': '2018-02-01',
                'end_date': '2019-02-01',
                'still_working': False,
            },
        )
        expected_sum_work = 'Feb 2018 - Feb 2019 - 1 yr 0 mos'
        self.assertEqual(response.data['sum_work'], expected_sum_work)

    def test_validate_create_duplicate_project(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        response = self.client.post(
            path=reverse("experience:project_CR", args=[self.experience.slug]),
            data={
                'name': 'Portfolio Backend Api',
                'description': 'an open source api project with Django & Drf',
                'stacks': [{'stack1': 'python', 'stack2': 'postgres'}]
            },
        )
        validate_txt = 'project with this name exists.'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], validate_txt)

    def test_validate_create_duplicate_reference(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token2}")
        response = self.client.post(
            path=reverse("experience:reference-list"),
            data={
                'full_name': 'Guido van Rossum',
                'email': 'Guido1987@email.com',
                'linkedin': 'https://www.linkedin.com/in/guido-van-rossum-4a0756',
                'recommendation': 'Lorem Ipsum is simply dummy text of the printing'
            },
        )
        validate_txt = 'someone with this full_name and email exists.'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], validate_txt)

    def test_validate_create_duplicate_personal_project(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token1}")
        response = self.client.post(
            path=reverse("experience:personal_project-list"),
            data={
                'name': 'RestApi-Blog',
                'stacks': [{'stack1': 'python', 'stack2': 'django'}],
                'description': 'Blog Project With Django and Drf',
            },
        )
        validate_txt = 'project with this name exists.'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], validate_txt)

    def test_validate_create_duplicate_blog(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"api-key {self.token3}")
        response = self.client.post(
            path=reverse("experience:blog-list"),
            data={
                'title': 'Commit Like a Pro',
                'description': 'Committing changes is one of the common things that',
                'link': 'https://imsadra.me/commit-like-a-pro'
            },
        )
        validate_txt = 'blog with this title exists.'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], validate_txt)
