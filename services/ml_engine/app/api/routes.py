"""API routers for the machine learning engine service."""

from fastapi import APIRouter


router = APIRouter()


@router.post("/ml/score", tags=["ml"])
async def score_email(message_id: str) -> dict[str, float | str]:
    """Return a placeholder risk score for the provided message ID."""

    # TODO: Integrate real model inference pipeline.
    return {"message_id": message_id, "score": 0.0, "confidence": 0.0}


@router.get("/ml/models", tags=["ml"])
async def list_models() -> dict[str, list[dict[str, str]]]:
    """List deployed models and metadata."""

    # TODO: Pull from model registry.
    return {"models": []}

