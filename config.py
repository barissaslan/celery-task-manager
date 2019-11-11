import logging
import os
from logging.handlers import RotatingFileHandler

from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
LOG_PATH = 'logs/app.log'
LOG_FORMATTER = '%(asctime)s %(filename)s %(funcName)12s() %(levelname)s %(message)s'


def make_celery():
    celery = Celery('tasks')
    celery.config_from_object(CeleryConfig)
    return celery


class CeleryConfig:
    broker_url = CELERY_BROKER_URL
    broker_pool_limit = 1
    broker_connection_timeout = 30
    broker_heartbeat = None
    event_queue_expires = 60  # Will delete all celeryev. queues without consumers after 1 minute.
    worker_prefetch_multiplier = 1  # Disable prefetching, it's causes problems and doesn't help performance


def get_logger():
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(LOG_FORMATTER))
    file_handler.setLevel(logging.INFO)

    logger = logging.getLogger('celery_application')
    logger.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    return logger
