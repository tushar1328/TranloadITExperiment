import os
import uuid

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from streaming.tasks import process_streaming_and_upload_to_s3
from streaming.validators import file_size

User = get_user_model()


# Create your models here.
class Stream(models.Model):
    id = models.UUIDField(
        uuid.uuid4,
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    file = models.FileField(
        validators=[validators.FileExtensionValidator(allowed_extensions=['mp3', 'mp4']),file_size],
        null=False,
        blank=False,
    )
    streaming_url = models.URLField(
        max_length=5000,
        null=False,
        blank=False
    )
    ext = models.CharField(
        max_length=20,
        default=None,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.file.url} || {self.ext} || {self.user}"

    def save(self, *args, **kwargs):
        name, extension = os.path.splitext(self.file.name)
        self.ext = extension
        super(Stream, self).save(*args, **kwargs)


@receiver(post_save, sender=Stream)
def process_stream(sender, instance, created, **kwargs):
    if created:
        process_streaming_and_upload_to_s3.delay(
            str(instance.id),
            str(instance.file.url),
            str(instance.ext),
            slugify(instance.file.name.split('.')[0])
        )