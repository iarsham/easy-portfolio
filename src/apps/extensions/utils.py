from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from os.path import basename, splitext


def filename_extract(file):
    base = basename(file)
    name, suffix = splitext(base)
    return name, suffix


def upload_file_path(instance, filename):
    name, suffix = filename_extract(filename)
    year = datetime.today().strftime("%Y-%m-%d")
    return f"{instance._meta.model_name}/{instance}/{name}-{year}{suffix}"


def validate_file_size(value):
    max_size = 2 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(
            _("You cannot upload file more than 2Mb")
        )
    return value
