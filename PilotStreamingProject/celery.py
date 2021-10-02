import os

from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PilotStreamingProject.settings')

app = Celery('PilotStreamingProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()