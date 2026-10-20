import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_liveness(async_client: AsyncClient):
    """Tests the /api/v1/health endpoint."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["app_name"] == "LABREX Intelligence Platform"
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_health_readiness(async_client: AsyncClient):
    """Tests the /api/v1/health/ready endpoint."""
    response = await async_client.get("/api/v1/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "READY"
    assert "database" in data["components"]


@pytest.mark.asyncio
async def test_root_metadata(async_client: AsyncClient):
    """Tests the root endpoint metadata response."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "platform" in data
    assert data["docs"] == "/docs"
