from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metaKeys.settings')

app = Celery('metaKeys')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-expired-checkin-data-every-night': {
        'task': 'users.tasks.delete_expired_checkin_data',
        'schedule': crontab(hour=3, minute=0),  # Esegui ogni notte alle 3:00
    },
}