"""API routers for the ingestion service."""

from fastapi import APIRouter


router = APIRouter()


@router.post("/gmail/push/webhook", status_code=204, tags=["gmail"])
async def gmail_push_webhook() -> None:
    """Handle Gmail push notifications.

    Note: Implementation will validate Google-signed JWT tokens, fetch message
    IDs, and dispatch Celery tasks for message retrieval.
    """


@router.post("/emails/{message_id}/ingest", tags=["emails"])
async def ingest_email(message_id: str) -> dict[str, str]:
    """Trigger ingestion workflow for the specified Gmail message ID."""

    # Placeholder response until workflow wiring is implemented.
    return {"message_id": message_id, "status": "queued"}

