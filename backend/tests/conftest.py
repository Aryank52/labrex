import pytest
from httpx import AsyncClient, ASGITransport
from backend.app.main import app


from backend.app.core.database import engine


@pytest.fixture(autouse=True)
async def cleanup_database_connections():
    """Ensure asyncpg engine connection pool is disposed cleanly between async tests."""
    yield
    await engine.dispose()


@pytest.fixture
async def async_client():
    """Async HTTP test client bound to FastAPI application."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

