from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.views import APIView, status, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from apps.users.api.serializers import UserDetailSerializer, UserUpdateSerializer

User = get_user_model()


class UserGetPatchDeleteApiView(ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @action(detail=True, methods=["get"])
    def retrieve_user(self, request):
        serializer = self.get_serializer(instance=self.get_object())
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["patch"])
    def update_user(self, request):
        serializer = self.get_serializer(
            instance=self.get_object(),
            data=request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["delete"])
    def delete_user(self, request):
        user = self.get_object()
        user.delete()
        return Response(
            {"message": "user deleted!"},
            status=status.HTTP_204_NO_CONTENT
        )

    def get_serializer_class(self):
        if self.action == "retrieve_user":
            return UserDetailSerializer
        return UserUpdateSerializer


class GoogleLoginApiView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.CALLBACK_URL_GOOGLE


class GithubLoginApiView(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.CALLBACK_URL_GITHUB
