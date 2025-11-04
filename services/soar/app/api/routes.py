"""API routers for the SOAR automation service."""

from fastapi import APIRouter


router = APIRouter()


@router.post("/soar/playbooks/{playbook_id}/trigger", tags=["soar"])
async def trigger_playbook(playbook_id: str) -> dict[str, str]:
    """Trigger the specified automation playbook."""

    return {"playbook_id": playbook_id, "status": "accepted"}

