import os

import django

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()


__all__ = ('celery_app',)
