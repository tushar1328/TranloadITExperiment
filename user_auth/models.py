import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(
        uuid.uuid4,
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
