"""API routers for the sandbox orchestration service."""

from fastapi import APIRouter


router = APIRouter()


@router.post("/sandbox/run", tags=["sandbox"])
async def run_sandbox(url: str, message_id: str | None = None) -> dict[str, str]:
    """Schedule a sandbox execution for the supplied URL."""

    # TODO: Dispatch sandbox task to orchestrator.
    return {"sandbox_id": "sandbox-placeholder", "status": "scheduled"}


@router.get("/sandbox/{sandbox_id}", tags=["sandbox"])
async def get_sandbox(sandbox_id: str) -> dict[str, str]:
    """Retrieve sandbox status and artifact metadata."""

    return {"sandbox_id": sandbox_id, "status": "pending"}

