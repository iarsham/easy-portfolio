from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from rest_framework.authentication import TokenAuthentication
from decouple import config


class ApiKeyAuthentication(TokenAuthentication):
    keyword = 'api-key'


class CustomAllAuthAdaptor(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        url = reverse("account_confirm_email", args=[emailconfirmation.key])
        return f"{config('FRONTEND_URL')}{url}"
