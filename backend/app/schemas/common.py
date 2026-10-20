from datetime import datetime, timezone
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorResponse(BaseModel):
    """RFC 7807 standard error response contract."""
    error_code: str = Field(..., description="Machine-readable error enum from ERROR_CATALOG")
    message: str = Field(..., description="Human-readable explanation of error")
    details: Dict[str, Any] = Field(default_factory=dict, description="Diagnostic details or field errors")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    request_id: Optional[str] = Field(default=None, description="Unique trace request ID")
    status_code: int = Field(..., description="HTTP status code")


class HealthStatusResponse(BaseModel):
    """System health and readiness probe response."""
    status: str = "HEALTHY"
    app_name: str
    version: str
    environment: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    components: Dict[str, str] = Field(default_factory=dict)


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard pagination wrapper for list endpoints."""
    items: List[T]
    total_count: int
    page: int
    page_size: int
    total_pages: int
