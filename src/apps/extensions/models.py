from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from apps.extensions.utils import upload_file_path
from apps.extensions.utils import validate_file_size


class AbstractTime(models.Model):
    created = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        abstract = True


class AbstractImage(models.Model):
    image = models.ImageField(
        verbose_name=_("Image"),
        null=False,
        upload_to=upload_file_path,
        validators=[
            validate_file_size,
            FileExtensionValidator(
                allowed_extensions=['png', 'jpeg', 'jpg'],
            )
        ]
    )

    class Meta:
        abstract = True


class AbstractCertificate(models.Model):
    certificate = models.FileField(
        verbose_name=_("Certificate"),
        null=False,
        upload_to=upload_file_path,
    )

    class Meta:
        abstract = True


class AbstractFile(models.Model):
    file = models.FileField(
        verbose_name=_("File"),
        null=False,
        upload_to=upload_file_path,
    )

    class Meta:
        abstract = True
