import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_backend.settings')

app = Celery('game_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'reset-leaderboard-every-sunday-midnight-est': {
        'task': 'game_app.tasks.reset_leaderboard',
        'schedule': crontab(minute=0, hour=5, day_of_week=0),  # 5 AM UTC = 12 AM EST
    },
}
