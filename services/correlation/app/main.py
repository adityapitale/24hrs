"""Correlation and reporting service FastAPI application entrypoint."""

from fastapi import FastAPI

from .api.routes import router as api_router


def create_app() -> FastAPI:
    """Create the FastAPI application instance."""

    app = FastAPI(title="PhishGuard Correlation Service", version="0.1.0")

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(api_router)

    return app


app = create_app()

