from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from allauth.account.models import EmailAddress

User = get_user_model()


class GeneralApiTestCase(APITestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_superuser(
            username='username1',
            email='username1@email.com',
            password='user1password'
        )
        self.token1 = self.user1.auth_token.key
        EmailAddress.objects.create(
            user=self.user1,
            email=self.user1.email,
            primary=True,
            verified=True
        )

        self.user2 = get_user_model().objects.create_user(
            username='username2',
            email='username2@email.com',
            password='user2password'
        )
        self.token2 = self.user2.auth_token.key
        EmailAddress.objects.create(
            user=self.user2,
            email=self.user2.email,
            primary=True,
            verified=True
        )

        self.user3 = get_user_model().objects.create_user(
            username='username3',
            email='username3@email.com',
            password='user3password'
        )
        self.token3 = self.user3.auth_token.key
        EmailAddress.objects.create(
            user=self.user3,
            email=self.user3.email,
            primary=True,
            verified=True
        )


class ExperienceApiTestCase(GeneralApiTestCase):

    def setUp(self):
        super().setUp()
        self.experience = self.user1.experience_user.create(
            role='Python Backend Developer',
            employment_type='full-time',
            company_name='Booking.com',
            start_date='2018-02-01',
            still_working=True
        )
        self.project = self.experience.experience_project.create(
            name='Portfolio Backend Api',
            description='an open source api project with Django & Drf',
            stacks=[{'stack1': 'python', 'stack2': 'postgres'}]
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


class PortfolioApiTestCase(GeneralApiTestCase):

    def setUp(self):
        super().setUp()
        self.aboutme = self.user1.user_aboutme
        self.aboutme2 = self.user2.user_aboutme
        self.aboutme3 = self.user3.user_aboutme
        self.aboutme_profile = self.aboutme.aboutme_profile.create()

        self.skill = self.aboutme.about_skill.create(
            name='python',
        )
        self.skill_certificate = self.skill.skill_certificate.create()

        self.language = self.aboutme2.about_language.create(
            name='Germany',
            proficiency='elementary',
        )
        self.language_certificate = self.language.language_certificate.create()

        self.achievement = self.aboutme3.about_achieve.create(
            title='django-achievements - Django App for user',
            description='Lorem Ipsum is simply dummy text of the printing ...',
        )
        self.achievement_certificate = self.achievement.achievement_certificate.create()
