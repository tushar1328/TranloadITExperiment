from django.core.exceptions import ValidationError


def file_size(value): # add this to some file where you can import it from
    limit = 6 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')