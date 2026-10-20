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
async def test_health_readiness(async_client: AsyncClient, monkeypatch):
    """Tests the /api/v1/health/ready endpoint with mocked successful DB check."""
    from unittest.mock import AsyncMock, MagicMock
    from backend.app.api.v1 import health

    mock_conn = AsyncMock()
    mock_res_1 = MagicMock()
    mock_res_1.scalar.return_value = 1
    mock_res_mig = MagicMock()
    mock_res_mig.scalar.return_value = "0001_initial_schema"
    mock_conn.execute.side_effect = [mock_res_1, mock_res_mig]

    mock_ctx = AsyncMock()
    mock_ctx.__aenter__.return_value = mock_conn

    mock_engine = MagicMock()
    mock_engine.connect.return_value = mock_ctx

    monkeypatch.setattr(health, "engine", mock_engine)

    response = await async_client.get("/api/v1/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "READY"
    assert data["components"]["database"] == "CONNECTED"


@pytest.mark.asyncio
async def test_root_metadata(async_client: AsyncClient):
    """Tests the root endpoint metadata response."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "platform" in data
    assert data["docs"] == "/docs"
