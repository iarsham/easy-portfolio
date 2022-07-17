from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView, status, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserDetailSerializer, UserUpdateSerializer

User = get_user_model()


class UserDetailApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        serializer = UserDetailSerializer(self.get_object())
        return Response(serializer.data, status.HTTP_200_OK)


class UserUpdateApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = UserUpdateSerializer(self.get_object(), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserDeleteApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": "user deleted!"}, status.HTTP_204_NO_CONTENT)


class RevokeApiKeyView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        old, new = get_object_or_404(Token, user=user).delete(), Token.objects.create(user=user)
        return Response({"key is revoked": new.key}, status.HTTP_201_CREATED)
