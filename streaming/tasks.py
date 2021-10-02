import random

import ffmpeg_streaming
import urllib3.util
from celery import shared_task
from django.conf import settings
from ffmpeg_streaming import CloudManager, Formats, Representation, Size, Bitrate
from ffmpeg_streaming import S3


@shared_task
def process_streaming_and_upload_to_s3(instance_id, file_url, ext,file_name):
    from streaming.models import Stream

    key = urllib3.util.parse_url(file_url)
    s3 = S3(
        aws_access_key_id=f'{settings.AWS_S3_ACCESS_KEY_ID}',
        aws_secret_access_key=f'{settings.AWS_S3_SECRET_ACCESS_KEY}',
        region_name=f'{settings.AWS_S3_REGION}'
    )
    streaming_file = ffmpeg_streaming.input(s3, bucket_name=f"{settings.AWS_STORAGE_BUCKET_NAME}", key=f"{(key.path)[1:]}")
    output_url = f'/hlsdemooutput/{random.randint(111111111, 999999999)}/{file_name}'
    save_to_s3 = CloudManager().add(s3, bucket_name=f"{settings.AWS_STORAGE_BUCKET_NAME}",folder=output_url,file_name="stream.m3u8")
    hls = streaming_file.hls(Formats.h264())
    if ext == ".mp3":
        _144p = Representation(Size(0, 0), Bitrate(95 * 1024, 64 * 1024))
        hls.representations(_144p)
    else:
        hls.auto_generate_representations()
    hls.output(clouds=save_to_s3)
    stream = Stream.objects.get(id=instance_id)
    stream.streaming_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}{output_url}/stream.m3u8'
    stream.save()

