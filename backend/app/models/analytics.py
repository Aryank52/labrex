import uuid
from datetime import date, datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import (
    BigInteger, Integer, Float, String, Date, DateTime, Boolean, ForeignKey, CheckConstraint, Index, Numeric, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.models.base import Base, TimestampMixin


class ForecastRun(Base):
    """Execution record for time-series forecasting pipeline runs."""
    __tablename__ = "forecast_run"

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    run_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="SUCCESS", nullable=False)
    execution_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    parameters: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ForecastDemand(Base, TimestampMixin):
    """Projected future labour demand with 80% and 95% uncertainty intervals."""
    __tablename__ = "forecast_demand"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("forecast_run.run_id", ondelete="CASCADE"), nullable=False, index=True)
    district_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_district.district_id", ondelete="RESTRICT"), nullable=False, index=True)
    occupation_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_occupation.occupation_id", ondelete="RESTRICT"), nullable=False, index=True)
    
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    horizon_months: Mapped[int] = mapped_column(Integer, nullable=False)
    
    point_estimate: Mapped[float] = mapped_column(Float, nullable=False)
    lower_bound_80: Mapped[float] = mapped_column(Float, nullable=False)
    upper_bound_80: Mapped[float] = mapped_column(Float, nullable=False)
    lower_bound_95: Mapped[float] = mapped_column(Float, nullable=False)
    upper_bound_95: Mapped[float] = mapped_column(Float, nullable=False)
    
    model_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_champion: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint("horizon_months IN (3, 6, 12, 18, 24)", name="chk_demand_forecast_horizon_valid"),
        CheckConstraint("point_estimate >= 0", name="chk_demand_forecast_non_neg"),
        Index("idx_forecast_demand_lookup", "district_id", "occupation_id", "horizon_months", "is_champion"),
    )


class ForecastSupply(Base, TimestampMixin):
    """Projected future workforce supply based on stock and certified trainee pipelines."""
    __tablename__ = "forecast_supply"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("forecast_run.run_id", ondelete="CASCADE"), nullable=False, index=True)
    district_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_district.district_id", ondelete="RESTRICT"), nullable=False, index=True)
    occupation_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_occupation.occupation_id", ondelete="RESTRICT"), nullable=False, index=True)
    
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    horizon_months: Mapped[int] = mapped_column(Integer, nullable=False)
    
    point_estimate: Mapped[float] = mapped_column(Float, nullable=False)
    lower_bound_80: Mapped[float] = mapped_column(Float, nullable=False)
    upper_bound_80: Mapped[float] = mapped_column(Float, nullable=False)
    lower_bound_95: Mapped[float] = mapped_column(Float, nullable=False)
    upper_bound_95: Mapped[float] = mapped_column(Float, nullable=False)
    
    model_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_champion: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint("horizon_months IN (3, 6, 12, 18, 24)", name="chk_supply_forecast_horizon_valid"),
        CheckConstraint("point_estimate >= 0", name="chk_supply_forecast_non_neg"),
        Index("idx_forecast_supply_lookup", "district_id", "occupation_id", "horizon_months", "is_champion"),
    )


class SkillGap(Base):
    """Computed net skill deficit or surplus with transparent index components."""
    __tablename__ = "skill_gap"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    district_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_district.district_id", ondelete="RESTRICT"), nullable=False, index=True)
    occupation_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_occupation.occupation_id", ondelete="RESTRICT"), nullable=False, index=True)
    horizon_months: Mapped[int] = mapped_column(Integer, nullable=False)
    
    demand_index: Mapped[float] = mapped_column(Float, nullable=False)
    supply_index: Mapped[float] = mapped_column(Float, nullable=False)
    projected_gap: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    gap_growth_rate: Mapped[float] = mapped_column(Float, default=0.0)
    
    confidence_score: Mapped[float] = mapped_column(Float, default=0.85)
    model_agreement: Mapped[str] = mapped_column(String(20), default="HIGH")
    risk_class: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        CheckConstraint("demand_index >= 0.0 AND demand_index <= 100.0", name="chk_gap_demand_index_range"),
        CheckConstraint("supply_index >= 0.0 AND supply_index <= 100.0", name="chk_gap_supply_index_range"),
        CheckConstraint("confidence_score >= 0.0 AND confidence_score <= 1.0", name="chk_gap_confidence_range"),
        Index("idx_skill_gap_geo_occ_horizon", "district_id", "occupation_id", "horizon_months", unique=True),
    )


class RiskAlert(Base):
    """LABREX RADAR early warnings for emerging shortages and skill shocks."""
    __tablename__ = "risk_alert"

    alert_id: Mapped[str] = mapped_column(String(50), primary_key=True)  # e.g., 'ALT-9042'
    district_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_district.district_id", ondelete="RESTRICT"), nullable=False, index=True)
    occupation_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_occupation.occupation_id", ondelete="RESTRICT"), nullable=False, index=True)
    
    risk_class: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # CRITICAL, HIGH, EMERGING, WATCH, OVERSUPPLY
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    trigger_drivers: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        Index("idx_risk_alert_active_class", "is_active", "risk_class"),
    )
