import os
from celery import Celery

celery = Celery(
    "app",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL"),
    broker_connection_retry_on_startup=True,
    broker_transport_options = {"max_retries": 10},
    include=["tasks"]
)