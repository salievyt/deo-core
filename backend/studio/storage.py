from pathlib import Path
from uuid import uuid4
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class PrivateLeadStorage(FileSystemStorage):
    @property
    def base_location(self):
        return settings.PRIVATE_MEDIA_ROOT

    @property
    def location(self):
        return str(Path(self.base_location).resolve())

    def url(self, name):
        raise ValueError("Lead attachments do not have public URLs.")


private_storage = PrivateLeadStorage()


def attachment_path(instance, filename):
    return f"leads/{instance.pk}/{uuid4().hex}{Path(filename).suffix.lower()}"


def image_path(instance, filename):
    return (
        f"cms/{instance._meta.model_name}/{uuid4().hex}{Path(filename).suffix.lower()}"
    )
