import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'proj.settings')

app = Celery('proj')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every': {
        'task': 'bot.tasks.update_currency_rates',
        'schedule': crontab(hour='*'),
    },
}
