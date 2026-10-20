from backend.app.core.config import settings


def test_default_settings():
    """Validates baseline platform settings and horizons."""
    assert settings.APP_NAME == "LABREX Intelligence Platform"
    assert settings.APP_VERSION == "1.0.0"
    assert settings.API_V1_PREFIX == "/api/v1"
    assert 12 in settings.FORECAST_HORIZONS
    assert settings.OPTIMIZATION_TIMEOUT_SECONDS > 0
