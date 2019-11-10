import logging
import os
import time
from logging.handlers import RotatingFileHandler

import requests
from flask import Flask, jsonify

from celery_config import make_celery

app = Flask(__name__)

celery = make_celery(app)

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

app.logger.info('Calculate Service Started')


@celery.task(name="multiply")
def multiply(x, y):
    result = x * y + 0.1
    time.sleep(3)

    url = 'http://127.0.0.1:5000/callback'
    data = {'result': result}

    requests.post(url, json=data)

    print("result:", result)

    return jsonify({'result': result})


if __name__ == "__main__":
    app.run()
