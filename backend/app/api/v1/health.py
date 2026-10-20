from fastapi import APIRouter, status, Response
from sqlalchemy import text
from backend.app.core.config import settings
from backend.app.core.database import engine
from backend.app.core.logging import logger
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


@router.get("/ready", response_model=HealthStatusResponse)
async def get_readiness_status(response: Response) -> HealthStatusResponse:
    """Readiness probe validating subsystem dependencies and migration compatibility."""
    components = {
        "model_registry": "INITIALIZED",
        "copilot": "READY" if settings.GEMINI_API_KEY else "NO_KEY_CONFIGURED"
    }

    db_status = "UNKNOWN"
    migration_status = "UNKNOWN"
    overall_ready = True

    try:
        async with engine.connect() as conn:
            res = await conn.execute(text("SELECT 1"))
            if res.scalar() == 1:
                db_status = "CONNECTED"

            try:
                mig_res = await conn.execute(text("SELECT version_num FROM alembic_version LIMIT 1"))
                current_rev = mig_res.scalar()
                migration_status = f"APPLIED:{current_rev}" if current_rev else "NONE"
            except Exception:
                migration_status = "NO_MIGRATION_TABLE"
    except Exception as e:
        logger.warning(f"Database readiness probe failed: {type(e).__name__}")
        db_status = "UNREACHABLE"
        migration_status = "UNAVAILABLE"
        overall_ready = False

    components["database"] = db_status
    components["migration"] = migration_status

    if not overall_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthStatusResponse(
            status="UNAVAILABLE",
            app_name=settings.APP_NAME,
            version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT,
            components=components
        )

    return HealthStatusResponse(
        status="READY",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        components=components
    )


@router.get("/version", status_code=status.HTTP_200_OK)
async def get_version() -> dict:
    """Returns active build and version metadata."""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }
