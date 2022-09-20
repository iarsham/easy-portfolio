from django.contrib.auth import get_user_model
from rest_framework import mixins, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.test import APITestCase
from allauth.account.models import EmailAddress

User = get_user_model()


class BaseViewSetMixin(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_create(self, serializer):
        serializer.save(about_me=self.get_object())


class BaseUpdateDeleteMixin(mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BlogPagination(PageNumberPagination):
    page_size = 3


class GerneralApiTestCase(APITestCase):
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
