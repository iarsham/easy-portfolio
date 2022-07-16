import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from extensions.models import AbstractTime


class User(AbstractUser, AbstractTime):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    email = models.EmailField(_("email address"), unique=True, null=False, blank=True)
    phone_number = PhoneNumberField(_("phone number"), null=True, blank=True)
    socials = models.JSONField(_("Socials Media"), default=dict, null=True, blank=True)
    created = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        if self.phone_number:
            return f"{self.email} : {self.phone_number}"
        return f"{self.email}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('last_login', 'updated')
