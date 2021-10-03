import os

from django.core.exceptions import ValidationError


def file_size(value):
    name, extension = os.path.splitext(value.name)
    if extension == '.mp4':
        limit = 18 * 1024 * 1024
        if value.size > limit:
            raise ValidationError('File too large. Size should not exceed 18 MiB.')
    else:
        limit = 6 * 1024 * 1024
        if value.size > limit:
            raise ValidationError('File too large. Size should not exceed 5 MiB.')
