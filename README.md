# Celery Distributed Task Manager Application

A basic Celery task manager application. 

## Installation

```bash
git clone git@github.com:barissaslan/celery-task-manager.git
```

### Docker Build 

```bash
docker build . -t celery-task-manager
```

### Docker Start 

```bash
docker run --network='host' celery-task-manager
```

### Python Setup

#### Installing Requirements

```bash
pip install -r requirements.txt
```

#### Set Environment Variables

```bash
export CELERY_BROKER_URL='celery broker url'
export CALLBACK_URL='callback url'
```

### Python Run

```bash
celery -A app.celery worker --without-gossip --without-mingle --without-heartbeat
```

### Run Unit Tests

```bash
python3 tests.py
```
