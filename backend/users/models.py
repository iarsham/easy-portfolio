import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from extensions.models import AbstractTime


class User(AbstractUser, AbstractTime):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(_("email address"), unique=True, null=False, blank=True)
    created = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} | {self.username}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('last_login', 'updated')
