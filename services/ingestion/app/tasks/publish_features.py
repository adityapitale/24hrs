"""Celery tasks for publishing emails to the feature extraction pipeline."""

from __future__ import annotations

import logging

from ..celery_app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(name="ingestion.extract_features")
def extract_features(email_id: int) -> bool:
    """Stub task that will forward email IDs to the feature extraction service."""

    logger.info("Queued feature extraction for email_id=%s", email_id)
    # TODO: hand off to feature extraction service when available.
    return True

