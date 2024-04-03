
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'POC_project_v2.settings')

app = Celery('POC_project_v2',)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = 'redis://localhost:6379'
app.conf.enable_utc = False

# app.conf.update(timezone='Europe/Paris')

app.autodiscover_tasks()
