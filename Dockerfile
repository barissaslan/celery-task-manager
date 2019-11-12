FROM python:3.7.4-alpine

COPY . /opt/celery-task-manager
WORKDIR /opt/celery-task-manager

ENV CELERY_BROKER_URL 'amqp://pyizcpcy:i8-DLpC9lKVReHWD0--fNDPT_QOJzNCJ@orangutan.rmq.cloudamqp.com/pyizcpcy'
ENV CALLBACK_URL 'http://127.0.0.1:8080/callback/{}'

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT celery -A app.celery worker --without-gossip --without-mingle --without-heartbeat