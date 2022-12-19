import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabrique_mailing.settings')

app = Celery('fabrique_mailing')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
