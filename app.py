import logging
import os
import time

import requests

from config import get_logger, make_celery

logger = get_logger()
celery = make_celery()

CALLBACK_URL = os.environ.get('CALLBACK_URL')

logging.info('Celery distributed task manager service starting..')


@celery.task(name="tasks.multiply")
def multiply(x, y):
    logger.info('Received x: {}, y: {} for the calculation'.format(x, y))

    try:
        result = x * y
    except TypeError:
        logger.error('<TypeError> error occurred when {} * {}'.format(x, y))
        return
    except Exception:
        logger.error('An error occurred when {} * {}'.format(x, y))
        return

    logger.info('Result of {} * {} = {}. Sleep for 3 second...'.format(x, y, result))

    time.sleep(3)

    url = CALLBACK_URL.format(result)

    logger.info('Sleep done. Sending result={} to callback.'.format(result))

    requests.get(url)
