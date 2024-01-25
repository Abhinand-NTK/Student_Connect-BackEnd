# from __future__ import absolute_import, unicode_literals
# import os

# from celery import Celery
# from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basicSetup.settings')

# app = Celery('basicSetup')
# app.conf.enable_utc = False

# app.config_from_object(settings, namespace='CELERY')

# app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f"Request: {self.request!r}") 



# your_project/celery.py

from __future__ import absolute_import, unicode_literals

# from _future_ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studentconnect.settings")


# Create a Celery instance and configure it with the Django settings.
app = Celery("studentconnect")

# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)