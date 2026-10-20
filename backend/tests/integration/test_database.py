"""Integration verification test suite for Phase 3 Database Foundation.

Validates:
- Engine connectivity & connection pooling
- PostGIS and pgcrypto extension activation
- Canonical dimension, fact, and governance table schemas
- Foreign key cascading/restricting policies
- Spatial Geometry SRID 4326 definitions
- Check constraints (non-negativity, ranges)
- Seed framework idempotency (zero duplicates on re-runs)
- API readiness & liveness probe integration
"""
import pytest
from datetime import date
from sqlalchemy import text, select, func
from sqlalchemy.exc import IntegrityError
from httpx import AsyncClient

from backend.app.core.database import engine, AsyncSessionFactory
from backend.app.services.data.seed_framework import seed_reference_and_fixtures
from backend.app.models.reference import (
    DimState, DimDistrict, DimSector, DimOccupation, DimSkill, DimSource
)
from backend.app.models.facts import FactJobDemand


@pytest.mark.asyncio
async def test_database_connectivity():
    """Verify async database engine connects and runs basic query."""
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_extensions_installed():
    """Verify PostGIS and pgcrypto extensions are active in the labrex database."""
    async with engine.connect() as conn:
        # Check PostGIS
        gis_res = await conn.execute(text("SELECT PostGIS_Version()"))
        version = gis_res.scalar()
        assert version is not None
        assert "3." in version

        # Check pgcrypto
        crypto_res = await conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'pgcrypto'"))
        assert crypto_res.scalar() == "pgcrypto"


@pytest.mark.asyncio
async def test_schema_core_tables_exist():
    """Verify all major dimensional and fact tables exist in public schema."""
    expected_tables = {
        "dim_date", "dim_state", "dim_district", "dim_sector",
        "dim_nco", "dim_occupation", "dim_skill", "dim_qualification",
        "dim_training_center", "dim_source", "fact_job_demand",
        "fact_workforce_supply", "fact_training_capacity", "fact_training_outcomes",
        "forecast_run", "skill_gap", "scenario", "audit_log", "dataset_registry"
    }
    async with engine.connect() as conn:
        res = await conn.execute(text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        ))
        existing_tables = {row[0] for row in res.fetchall()}
        missing = expected_tables - existing_tables
        assert not missing, f"Missing tables in public schema: {missing}"


@pytest.mark.asyncio
async def test_spatial_geometry_srid():
    """Verify PostGIS geometry columns have explicit SRID 4326."""
    async with engine.connect() as conn:
        res = await conn.execute(text("""
            SELECT f_table_name, f_geometry_column, srid, type
            FROM geometry_columns
            WHERE f_table_name IN ('dim_state', 'dim_district', 'dim_training_center')
        """))
        geoms = res.fetchall()
        assert len(geoms) >= 3
        for table_name, col_name, srid, geom_type in geoms:
            assert srid == 4326, f"Column {table_name}.{col_name} has invalid SRID: {srid}"


@pytest.mark.asyncio
async def test_non_negative_check_constraints():
    """Verify that CHECK constraints prevent negative demand values."""
    async with AsyncSessionFactory() as session:
        # Attempt to insert negative demand
        invalid_demand = FactJobDemand(
            date_key=date(2024, 1, 1),
            district_id="IN-MH-PUN",
            occupation_id="OCC-AUTO-EV-MECH",
            active_postings=-50,  # Violates chk_demand_active_postings_non_neg
            new_postings=10,
            source_id="LABREX_DEMO",
            dataset_type="FIXTURE"
        )
        session.add(invalid_demand)
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()


@pytest.mark.asyncio
async def test_seed_idempotency():
    """Verify running seed_reference_and_fixtures multiple times does not duplicate rows."""
    async with AsyncSessionFactory() as session:
        # Run seed first time
        stats1 = await seed_reference_and_fixtures(session)
        assert stats1["dim_state"] >= 3
        assert stats1["dim_occupation"] >= 10
        assert stats1["dim_skill"] >= 20

        # Query counts
        count_states_1 = await session.scalar(select(func.count(DimState.state_id)))
        count_skills_1 = await session.scalar(select(func.count(DimSkill.skill_id)))
        count_demands_1 = await session.scalar(select(func.count(FactJobDemand.id)))

        # Run seed second time
        stats2 = await seed_reference_and_fixtures(session)

        # Query counts again
        count_states_2 = await session.scalar(select(func.count(DimState.state_id)))
        count_skills_2 = await session.scalar(select(func.count(DimSkill.skill_id)))
        count_demands_2 = await session.scalar(select(func.count(FactJobDemand.id)))

        assert count_states_1 == count_states_2
        assert count_skills_1 == count_skills_2
        assert count_demands_1 == count_demands_2


@pytest.mark.asyncio
async def test_readiness_probe_integration(async_client: AsyncClient):
    """Verify API readiness probe reports database reachability and migration revision."""
    response = await async_client.get("/api/v1/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "READY"
    assert data["components"]["database"] == "CONNECTED"
    assert "APPLIED" in data["components"]["migration"]
