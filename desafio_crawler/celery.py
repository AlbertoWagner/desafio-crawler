import os
from celery import Celery
from celery.signals import setup_logging

# Define a variável de ambiente DJANGO_SETTINGS_MODULE para o arquivo de configurações Django.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "desafio_crawler.settings")

# Crie uma instância do Celery chamada 'app'.
app = Celery("desafio_crawler")


# Configure os registradores de log. Este é um sinal que configura os registradores com
# base nas configurações do Django.
@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import (
        dictConfig,
    )  # Importa a função dictConfig para configurar os registradores.
    from django.conf import settings  # Importa as configurações do Django.

    # Configura os registradores com base nas configurações definidas em settings.LOGGING.
    dictConfig(settings.LOGGING)


# A função 'debug_task' é definida como uma tarefa de exemplo que imprime informações sobre a solicitação.
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# Descubra e registre automaticamente tarefas do Celery em seu projeto.
app.autodiscover_tasks()

# Configure a instância do Celery com base nas configurações do Django.
app.config_from_object("django.conf:settings", namespace="CELERY")
