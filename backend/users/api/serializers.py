from django.contrib.auth import get_user_model
from rest_framework import serializers
from allauth.account.models import EmailAddress


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class UserDetailSerializer(serializers.ModelSerializer):
    verify = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username',
            'email', 'verify',
        )

    def get_verify(self, obj):
        user = EmailAddress.objects.get(user_id=obj.id)
        return user.verified
