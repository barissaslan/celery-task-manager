import logging
import os
import time

import requests

from config import get_logger, make_celery

logger = get_logger()
celery = make_celery()

CALLBACK_URL = os.environ.get('CALLBACK_URL')
TYPE_ERROR_MESSAGE = '<TypeError> error occurred when {} * {}'

logging.info('Celery distributed task manager service starting..')


@celery.task(name="tasks.multiply")
def multiply(x, y):
    logger.info('Received x: {}, y: {} for the calculation'.format(x, y))

    try:
        result = x * y
    except TypeError:
        message = TYPE_ERROR_MESSAGE.format(x, y)
        logger.error(message)
        return {'error': message}
    except Exception as e:
        logger.error(str(e))
        return {'error': str(e)}

    logger.info('Result of {} * {} = {}. Sleep for 3 second...'.format(x, y, result))

    time.sleep(3)

    url = CALLBACK_URL.format(result)

    logger.info('Sleep done. Sending result={} to callback.'.format(result))

    try:
        requests.get(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)

    return {'result': result}
