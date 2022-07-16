from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from allauth.account.models import EmailAddress


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'username', 'first_name',
            'last_name', 'email',
            'phone_number', 'socials',
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    verify = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username',
            'full_name', 'email',
            'phone_number', "socials",
            'verify',
        ]

    def get_full_name(self, obj):
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return None

    def get_verify(self, obj):
        user = get_object_or_404(EmailAddress, user_id=obj.id)
        return user.verified
