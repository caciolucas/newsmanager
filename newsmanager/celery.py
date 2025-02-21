from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# Define o módulo de configurações do Django para o Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsmanager.settings")

app = Celery("newsmanager")

# Configura o Celery para usar as configurações do Django com o prefixo 'CELERY'
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover das tasks nos aplicativos Django registrados
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "publish-pending-news": {
        "task": "news.tasks.publish_pending_news",
        "schedule": crontab(minute="*/1"),
    },
}
