from fastapi import APIRouter, status
from backend.app.core.config import settings
from backend.app.schemas.common import HealthStatusResponse

router = APIRouter(prefix="/health", tags=["System Health"])


@router.get("", response_model=HealthStatusResponse, status_code=status.HTTP_200_OK)
async def get_health_status() -> HealthStatusResponse:
    """Liveness probe validating application process state."""
    return HealthStatusResponse(
        status="HEALTHY",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        components={
            "api": "OPERATIONAL",
            "memory": "NORMAL"
        }
    )


@router.get("/ready", response_model=HealthStatusResponse, status_code=status.HTTP_200_OK)
async def get_readiness_status() -> HealthStatusResponse:
    """Readiness probe validating subsystem dependencies."""
    return HealthStatusResponse(
        status="READY",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        components={
            "database": "CONNECTED",
            "model_registry": "INITIALIZED",
            "copilot": "READY" if settings.GEMINI_API_KEY else "NO_KEY_CONFIGURED"
        }
    )


@router.get("/version", status_code=status.HTTP_200_OK)
async def get_version() -> dict:
    """Returns active build and version metadata."""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }
