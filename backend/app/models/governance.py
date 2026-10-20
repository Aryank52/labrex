import uuid
from datetime import date, datetime, timezone
from typing import Optional, Dict, Any, List
from sqlalchemy import (
    BigInteger, Integer, Float, String, Date, DateTime, Boolean, ForeignKey, Index, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base


class DatasetRegistry(Base):
    """Metadata tracking for each ingested dataset batch, snapshot, or fixture."""
    __tablename__ = "dataset_registry"

    dataset_id: Mapped[str] = mapped_column(String(50), primary_key=True)  # e.g., 'DS-NCS-2025-10'
    source_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_source.source_id", ondelete="RESTRICT"), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), default="1.0")
    
    coverage_start: Mapped[Optional[date]] = mapped_column(Date)
    coverage_end: Mapped[Optional[date]] = mapped_column(Date)
    row_count: Mapped[int] = mapped_column(BigInteger, default=0)
    data_type: Mapped[str] = mapped_column(String(20), default="REAL", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")
    quality_score: Mapped[float] = mapped_column(Float, default=95.0)
    
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    quality_checks: Mapped[List["DataQuality"]] = relationship("DataQuality", back_populates="dataset")


class DataQuality(Base):
    """Automated schema validation, completeness, and outlier checks on datasets."""
    __tablename__ = "data_quality"

    check_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    dataset_id: Mapped[str] = mapped_column(String(50), ForeignKey("dataset_registry.dataset_id", ondelete="CASCADE"), nullable=False, index=True)
    check_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    completeness_pct: Mapped[float] = mapped_column(Float, default=100.0)
    valid_geometry_pct: Mapped[float] = mapped_column(Float, default=100.0)
    unmapped_nco_pct: Mapped[float] = mapped_column(Float, default=0.0)
    duplicate_count: Mapped[int] = mapped_column(Integer, default=0)
    passed: Mapped[bool] = mapped_column(Boolean, default=True)
    details: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    dataset: Mapped["DatasetRegistry"] = relationship("DatasetRegistry", back_populates="quality_checks")


class DataLineage(Base):
    """End-to-end data provenance connecting facts, models, and policy recommendations."""
    __tablename__ = "data_lineage"

    lineage_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    target_entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., 'FORECAST', 'GAP', 'INTERVENTION'
    target_entity_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    source_dataset_id: Mapped[str] = mapped_column(String(50), ForeignKey("dataset_registry.dataset_id", ondelete="RESTRICT"), nullable=False, index=True)
    transformation_pipeline: Mapped[str] = mapped_column(String(100), nullable=False)
    model_run_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AuditLog(Base):
    """Immutable audit trail of analytical operations, optimizations, and administrative actions."""
    __tablename__ = "audit_log"

    log_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource: Mapped[Optional[str]] = mapped_column(String(100))
    details: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ModelRegistry(Base):
    """Catalogue of trained forecasting, ML, and heuristic models."""
    __tablename__ = "model_registry"

    model_id: Mapped[str] = mapped_column(String(50), primary_key=True)  # e.g., 'LGBM_DEMAND_REGRESSOR_V1'
    model_type: Mapped[str] = mapped_column(String(50), nullable=False)   # 'TREE_ENSEMBLE', 'FOUNDATION_TS', 'HEURISTIC'
    algorithm_name: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(50), default="1.0")
    status: Mapped[str] = mapped_column(String(20), default="CANDIDATE", nullable=False, index=True)  # CANDIDATE, VALIDATED, CHAMPION, RETIRED, BLOCKED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    runs: Mapped[List["ModelRun"]] = relationship("ModelRun", back_populates="model")


class ModelRun(Base):
    """Specific training run and evaluation experiment for a registered model."""
    __tablename__ = "model_run"

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(50), ForeignKey("model_registry.model_id", ondelete="CASCADE"), nullable=False, index=True)
    training_dataset_version: Mapped[str] = mapped_column(String(50), nullable=False)
    hyperparameters: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    
    train_start: Mapped[date] = mapped_column(Date, nullable=False)
    train_end: Mapped[date] = mapped_column(Date, nullable=False)
    val_start: Mapped[date] = mapped_column(Date, nullable=False)
    val_end: Mapped[date] = mapped_column(Date, nullable=False)
    metrics: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    model: Mapped["ModelRegistry"] = relationship("ModelRegistry", back_populates="runs")
    metrics_list: Mapped[List["ModelMetric"]] = relationship("ModelMetric", back_populates="run", cascade="all, delete-orphan")


class ModelMetric(Base):
    """Granular benchmark metrics (WAPE, RMSE, Coverage) across geographic slices and horizons."""
    __tablename__ = "model_metric"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("model_run.run_id", ondelete="CASCADE"), nullable=False, index=True)
    metric_name: Mapped[str] = mapped_column(String(50), nullable=False)  # 'WAPE', 'MAE', 'RMSE', 'COVERAGE_80', 'COVERAGE_95'
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    horizon_months: Mapped[int] = mapped_column(Integer, nullable=False)
    slice_name: Mapped[str] = mapped_column(String(50), default="NATIONAL")

    run: Mapped["ModelRun"] = relationship("ModelRun", back_populates="metrics_list")

    __table_args__ = (
        Index("idx_model_metric_run_name_horizon", "run_id", "metric_name", "horizon_months"),
    )
