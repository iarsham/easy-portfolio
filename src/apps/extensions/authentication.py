import os
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.authentication import TokenAuthentication
from dj_rest_auth.serializers import PasswordResetSerializer
from dj_rest_auth.forms import AllAuthPasswordResetForm
from allauth.account import app_settings
from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str, user_username
from allauth.account.adapter import get_adapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri
from decouple import config


class ApiKeyAuthentication(TokenAuthentication):
    keyword = 'api-key'


class CustomAllAuthAdaptor(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        url = reverse("account_confirm_email", args=[emailconfirmation.key])
        slice_url = url.split('v1')[1]
        link = build_absolute_uri(None, slice_url, 'https')
        if os.getenv('DJANGO_SETTINGS_MODULE') == 'config.settings.development':
            return link
        else:
            return f"{config('FRONTEND_URL')}{slice_url}"


class CustomPasswordResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        for user in self.users:
            temp_key = token_generator.make_token(user)
            path = reverse(
                'password_reset_confirm',
                args=[user_pk_to_url_str(user), temp_key],
            )
            slice_url = path.split('v1')[1]
            if not os.getenv('DJANGO_SETTINGS_MODULE') == 'config.settings.development':
                url = f"{config('FRONTEND_URL')}{slice_url}"
            else:
                url = build_absolute_uri(None, slice_url, 'https')
            context = {
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'request': request,
            }
            if app_settings.AUTHENTICATION_METHOD != app_settings.AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context
            )
        return self.cleaned_data['email']


class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomPasswordResetForm
