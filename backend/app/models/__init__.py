"""
LABREX SQLAlchemy Model Registry.
Exposes Base and all dimensional, fact, analytical, scenario, and governance entities.
"""

from backend.app.models.base import Base, TimestampMixin

# Reference / Dimensions
from backend.app.models.reference import (
    DimDate,
    DimState,
    DimDistrict,
    DimSector,
    DimNco,
    DimOccupation,
    DimSkill,
    DimNsqfLevel,
    DimQualification,
    DimTrainingProgram,
    DimTrainingCenter,
    DimSource,
    MapOccupationSkill,
    MapSkillQualification,
    SkillTypeEnum,
    CenterTypeEnum,
    DataTypeEnum,
)

# Core Facts
from backend.app.models.facts import (
    FactJobDemand,
    FactWorkforceSupply,
    FactTrainingCapacity,
    FactTrainingOutcomes,
    FactSkillSignal,
    FactEmployerSignal,
)

# Analytical / Forecasting / Gaps
from backend.app.models.analytics import (
    ForecastRun,
    ForecastDemand,
    ForecastSupply,
    SkillGap,
    RiskAlert,
)

# Scenarios & Policy Optimization
from backend.app.models.scenarios import (
    Scenario,
    ScenarioResult,
    OptimizationRun,
    OptimizationResult,
)

# Governance & Audit
from backend.app.models.governance import (
    DatasetRegistry,
    DataQuality,
    DataLineage,
    AuditLog,
    ModelRegistry,
    ModelRun,
    ModelMetric,
)

__all__ = [
    "Base",
    "TimestampMixin",
    # Reference
    "DimDate",
    "DimState",
    "DimDistrict",
    "DimSector",
    "DimNco",
    "DimOccupation",
    "DimSkill",
    "DimNsqfLevel",
    "DimQualification",
    "DimTrainingProgram",
    "DimTrainingCenter",
    "DimSource",
    "MapOccupationSkill",
    "MapSkillQualification",
    "SkillTypeEnum",
    "CenterTypeEnum",
    "DataTypeEnum",
    # Facts
    "FactJobDemand",
    "FactWorkforceSupply",
    "FactTrainingCapacity",
    "FactTrainingOutcomes",
    "FactSkillSignal",
    "FactEmployerSignal",
    # Analytics
    "ForecastRun",
    "ForecastDemand",
    "ForecastSupply",
    "SkillGap",
    "RiskAlert",
    # Scenarios & Optimizer
    "Scenario",
    "ScenarioResult",
    "OptimizationRun",
    "OptimizationResult",
    # Governance
    "DatasetRegistry",
    "DataQuality",
    "DataLineage",
    "AuditLog",
    "ModelRegistry",
    "ModelRun",
    "ModelMetric",
]
