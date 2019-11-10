import time

import requests
from flask import Flask

from config import make_celery, set_logger

app = Flask(__name__)

celery = make_celery(app)

set_logger(app)

app.logger.info('Celery distributed task manager service starting..')


@celery.task(name="multiply")
def multiply(x, y):
    app.logger.info('Received x: {}, y: {} for the calculation'.format(x, y))

    try:
        result = x * y
    except TypeError:
        app.logger.error('<TypeError> error occurred when {} * {}'.format(x, y))
        return
    except Exception:
        app.logger.error('An error occurred when {} * {}'.format(x, y))
        return

    app.logger.info('Result of {} * {} = {}. Sleep for 3 second...'.format(x, y, result))

    time.sleep(3)

    url = 'http://127.0.0.1:5000/callback'
    data = {'result': result, 'x': x, 'y': y}

    app.logger.info('Sleep done. Sending result={} to callback.'.format(result))

    requests.post(url, json=data)


if __name__ == "__main__":
    app.run()
