from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://host.docker.internal:6379/0",
    backend="redis://host.docker.internal:6379/0"
)