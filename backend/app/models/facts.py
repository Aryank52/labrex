from datetime import date
from sqlalchemy import (
    BigInteger, Integer, Float, String, Date, ForeignKey, CheckConstraint, Index
)
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.models.base import Base, TimestampMixin


class FactJobDemand(Base, TimestampMixin):
    """Monthly observed / aggregated job posting demand signals by district and occupation."""
    __tablename__ = "fact_job_demand"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date_key: Mapped[date] = mapped_column(Date, ForeignKey("dim_date.date_key", ondelete="RESTRICT"), nullable=False, index=True)
    district_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_district.district_id", ondelete="RESTRICT"), nullable=False, index=True)
    occupation_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_occupation.occupation_id", ondelete="RESTRICT"), nullable=False, index=True)
    
    active_postings: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    new_postings: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    median_days_open: Mapped[int] = mapped_column(Integer, default=30)
    unique_employers: Mapped[int] = mapped_column(Integer, default=1)
    
    source_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_source.source_id", ondelete="RESTRICT"), nullable=False)
    dataset_type: Mapped[str] = mapped_column(String(20), default="REAL", nullable=False)

    __table_args__ = (
        CheckConstraint("active_postings >= 0", name="chk_demand_active_postings_non_neg"),
        CheckConstraint("new_postings >= 0", name="chk_demand_new_postings_non_neg"),
        CheckConstraint("unique_employers >= 0", name="chk_demand_employers_non_neg"),
        Index("idx_fact_demand_geo_occ_date", "district_id", "occupation_id", "date_key", unique=True),
    )


class FactWorkforceSupply(Base, TimestampMixin):
    """Estimated available workforce stock and labor supply pipeline."""
    __tablename__ = "fact_workforce_supply"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date_key: Mapped[date] = mapped_column(Date, ForeignKey("dim_date.date_key", ondelete="RESTRICT"), nullable=False, index=True)
    district_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_district.district_id", ondelete="RESTRICT"), nullable=False, index=True)
    occupation_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_occupation.occupation_id", ondelete="RESTRICT"), nullable=False, index=True)
    
    employed_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unemployed_seeking: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    fresh_graduates: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    source_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_source.source_id", ondelete="RESTRICT"), nullable=False)
    dataset_type: Mapped[str] = mapped_column(String(20), default="REAL", nullable=False)

    __table_args__ = (
        CheckConstraint("employed_stock >= 0", name="chk_supply_employed_stock_non_neg"),
        CheckConstraint("unemployed_seeking >= 0", name="chk_supply_unemployed_non_neg"),
        Index("idx_fact_supply_geo_occ_date", "district_id", "occupation_id", "date_key", unique=True),
    )


class FactTrainingCapacity(Base, TimestampMixin):
    """Sanctioned seats and trainee intake capacity at training centres."""
    __tablename__ = "fact_training_capacity"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date_key: Mapped[date] = mapped_column(Date, ForeignKey("dim_date.date_key", ondelete="RESTRICT"), nullable=False, index=True)
    center_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_training_center.center_id", ondelete="RESTRICT"), nullable=False, index=True)
    qualification_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_qualification.qualification_id", ondelete="RESTRICT"), nullable=False, index=True)
    
    sanctioned_seats: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    enrolled_trainees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    source_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_source.source_id", ondelete="RESTRICT"), nullable=False)
    dataset_type: Mapped[str] = mapped_column(String(20), default="REAL", nullable=False)

    __table_args__ = (
        CheckConstraint("sanctioned_seats >= 0", name="chk_capacity_seats_non_neg"),
        CheckConstraint("enrolled_trainees >= 0", name="chk_capacity_enrolled_non_neg"),
        Index("idx_fact_capacity_center_qual_date", "center_id", "qualification_id", "date_key", unique=True),
    )


class FactTrainingOutcomes(Base, TimestampMixin):
    """Training completions, certifications, and reported employment placements."""
    __tablename__ = "fact_training_outcomes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date_key: Mapped[date] = mapped_column(Date, ForeignKey("dim_date.date_key", ondelete="RESTRICT"), nullable=False, index=True)
    center_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_training_center.center_id", ondelete="RESTRICT"), nullable=False, index=True)
    qualification_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_qualification.qualification_id", ondelete="RESTRICT"), nullable=False, index=True)
    
    completed_trainees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    certified_trainees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    placed_trainees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    source_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_source.source_id", ondelete="RESTRICT"), nullable=False)
    dataset_type: Mapped[str] = mapped_column(String(20), default="REAL", nullable=False)

    __table_args__ = (
        CheckConstraint("completed_trainees >= 0", name="chk_outcomes_completed_non_neg"),
        CheckConstraint("certified_trainees >= 0", name="chk_outcomes_certified_non_neg"),
        CheckConstraint("placed_trainees >= 0", name="chk_outcomes_placed_non_neg"),
        Index("idx_fact_outcomes_center_qual_date", "center_id", "qualification_id", "date_key", unique=True),
    )


class FactSkillSignal(Base, TimestampMixin):
    """High-frequency granular skill keyword mentions and intensity momentum."""
    __tablename__ = "fact_skill_signal"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date_key: Mapped[date] = mapped_column(Date, ForeignKey("dim_date.date_key", ondelete="RESTRICT"), nullable=False, index=True)
    district_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_district.district_id", ondelete="RESTRICT"), nullable=False, index=True)
    skill_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_skill.skill_id", ondelete="RESTRICT"), nullable=False, index=True)
    
    frequency_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    growth_rate_mom: Mapped[float] = mapped_column(Float, default=0.0)
    intensity_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    source_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_source.source_id", ondelete="RESTRICT"), nullable=False)
    dataset_type: Mapped[str] = mapped_column(String(20), default="REAL", nullable=False)

    __table_args__ = (
        CheckConstraint("frequency_count >= 0", name="chk_skill_signal_frequency_non_neg"),
        Index("idx_fact_skill_geo_date", "district_id", "skill_id", "date_key", unique=True),
    )


class FactEmployerSignal(Base, TimestampMixin):
    """Aggregate enterprise hiring signals by sector and district."""
    __tablename__ = "fact_employer_signal"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date_key: Mapped[date] = mapped_column(Date, ForeignKey("dim_date.date_key", ondelete="RESTRICT"), nullable=False, index=True)
    district_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_district.district_id", ondelete="RESTRICT"), nullable=False, index=True)
    sector_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_sector.sector_id", ondelete="RESTRICT"), nullable=False, index=True)
    
    active_employers_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hiring_expansion_sentiment: Mapped[float] = mapped_column(Float, default=0.0)
    
    source_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_source.source_id", ondelete="RESTRICT"), nullable=False)
    dataset_type: Mapped[str] = mapped_column(String(20), default="REAL", nullable=False)

    __table_args__ = (
        CheckConstraint("active_employers_count >= 0", name="chk_employer_signal_count_non_neg"),
        Index("idx_fact_employer_geo_date", "district_id", "sector_id", "date_key", unique=True),
    )
