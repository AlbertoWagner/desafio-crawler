import os
from celery import Celery

# Configura a definição do Celery
# from celery.signals import setup_logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desafio_crawler.settings')
app = Celery('desafio_crawler')


# @setup_logging.connect
# def config_loggers(*args, **kwargs):
#     from logging.config import dictConfig  # noqa
#     from django.conf import settings  # noqa
#
#     dictConfig(settings.LOGGING)


# Load task modules from all registered Django app configs.

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.autodiscover_tasks()
app.config_from_object('django.conf:settings', namespace='CELERY')

# @setup_logging.connect
# def config_loggers(*args, **kwargs):
#     from logging.config import dictConfig  # noqa
#     from django.conf import settings  # noqa
#
#     dictConfig(settings.LOGGING)


# Load task modules from all registered Django app configs.

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.autodiscover_tasks()