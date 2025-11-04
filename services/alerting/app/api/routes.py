"""API routers for the alerting service."""

from fastapi import APIRouter


router = APIRouter()


@router.post("/alerts/notify", tags=["alerts"])
async def notify(channel: str) -> dict[str, str]:
    """Queue alert notifications for downstream delivery."""

    return {"channel": channel, "status": "queued"}


@router.websocket("/ws/alerts")
async def websocket_endpoint():
    """Placeholder WebSocket endpoint for real-time alert streaming."""

    # TODO: Implement with FastAPI's WebSocket support and Redis pub/sub.
    raise NotImplementedError("WebSocket handling not yet implemented")

