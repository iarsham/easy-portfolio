from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from allauth.account.models import EmailAddress
from apps.portfolio.models import AboutMe, Education


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
        obj = AboutMe.objects.create(user=instance)
        Education.objects.create(about_me=obj)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_email_verification(sender, instance, created, **kwargs):
    if not created:
        email_address_obj = EmailAddress.objects.get(user=instance)
        email_address_obj.email = instance.email
        email_address_obj.save()
