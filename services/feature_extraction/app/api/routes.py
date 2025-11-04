"""API routers for the feature extraction service."""

from fastapi import APIRouter


router = APIRouter()


@router.post("/features/extract", tags=["features"])
async def extract_features(message_id: str) -> dict[str, str]:
    """Placeholder endpoint for feature extraction pipeline triggering."""

    return {"message_id": message_id, "status": "processing"}


@router.get("/features/{message_id}", tags=["features"])
async def get_features(message_id: str) -> dict[str, str | float | int]:
    """Fetch cached feature vectors for the given message ID."""

    # TODO: Replace with datastore integration.
    return {"message_id": message_id, "features": {}, "status": "pending"}

