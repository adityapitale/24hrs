"""Celery application configuration for the ingestion service."""

from __future__ import annotations

from celery import Celery

from .deps import get_settings


settings = get_settings()

celery_app = Celery(
    "ingestion",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_default_queue="ingestion",
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    timezone="UTC",
)

# TODO: tighten Celery security settings (auth, TLS) for production deployments.

