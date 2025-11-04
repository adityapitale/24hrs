"""API routers for the correlation and reporting service."""

from fastapi import APIRouter


router = APIRouter()


@router.get("/incidents/{incident_id}", tags=["incidents"])
async def get_incident(incident_id: str) -> dict[str, str]:
    """Return incident overview data."""

    return {"incident_id": incident_id, "status": "draft"}


@router.post("/incidents/report", tags=["incidents"])
async def generate_report(incident_id: str) -> dict[str, str]:
    """Kick off report generation for the specified incident."""

    return {"incident_id": incident_id, "report": "pending"}

