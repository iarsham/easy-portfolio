import tempfile
from PIL import Image
from os.path import basename, splitext
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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


def create_test_image():
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)
    return tmp_file
