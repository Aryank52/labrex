import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from backend.app.core.config import settings
from backend.app.core.logging import setup_logging, logger
from backend.app.schemas.common import ErrorResponse
from backend.app.api.v1.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager handling startup and shutdown events."""
    setup_logging(level="DEBUG" if settings.DEBUG else "INFO")
    logger.info(f"Initializing {settings.APP_NAME} v{settings.APP_VERSION} [{settings.ENVIRONMENT}]")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Evidence-backed labour-market intelligence, workforce forecasting, and policy optimization platform.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    """Injects unique request_id and measures endpoint latency."""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    start_time = time.time()

    response = await call_next(request)

    latency_ms = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time"] = f"{latency_ms}ms"

    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code} ({latency_ms}ms)",
        extra={
            "request_id": request_id,
            "status_code": response.status_code,
            "latency_ms": latency_ms
        }
    )
    return response


# RFC 7807 Standard Error Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Formats validation errors into the standard RFC 7807 error schema."""
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    error_payload = ErrorResponse(
        error_code="VALIDATION_FAILED",
        message="Request payload or parameters violated validation constraints.",
        details={"errors": exc.errors()},
        request_id=request_id,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error_payload.model_dump(mode="json"))


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catches unhandled exceptions, logs traceback, and returns sanitized error."""
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    logger.error(f"Unhandled system error [Req {request_id}]: {exc}", exc_info=True)

    error_payload = ErrorResponse(
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected server error occurred. Please contact the administrator with the request ID.",
        details={},
        request_id=request_id,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_payload.model_dump(mode="json"))


# Mount API Routers
app.include_router(health_router, prefix="")
app.include_router(health_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root metadata redirect."""
    return {
        "platform": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health"
    }
