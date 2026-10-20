import enum
from typing import Optional, List
from datetime import date
from sqlalchemy import (
    String, Integer, Float, Boolean, Date, ForeignKey, CheckConstraint, Index, Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from backend.app.models.base import Base, TimestampMixin


class SkillTypeEnum(str, enum.Enum):
    TECHNICAL = "TECHNICAL"
    FOUNDATIONAL = "FOUNDATIONAL"
    DIGITAL = "DIGITAL"
    GREEN = "GREEN"


class CenterTypeEnum(str, enum.Enum):
    ITI = "ITI"
    PMKVY_KENDRA = "PMKVY_KENDRA"
    POLYTECHNIC = "POLYTECHNIC"
    PRIVATE_VTP = "PRIVATE_VTP"


class DataTypeEnum(str, enum.Enum):
    REAL = "REAL"
    DERIVED = "DERIVED"
    SYNTHETIC = "SYNTHETIC"
    FIXTURE = "FIXTURE"


class DimDate(Base):
    """Canonical temporal calendar dimension."""
    __tablename__ = "dim_date"

    date_key: Mapped[date] = mapped_column(Date, primary_key=True)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    quarter: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    financial_year: Mapped[str] = mapped_column(String(10), nullable=False)
    financial_quarter: Mapped[str] = mapped_column(String(10), nullable=False)
    month_name: Mapped[str] = mapped_column(String(20), nullable=False)
    is_weekend: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        Index("idx_dim_date_year_month", "year", "month"),
        Index("idx_dim_date_quarter", "quarter", "year"),
    )


class DimState(Base, TimestampMixin):
    """Administrative state or union territory dimension with spatial geometry."""
    __tablename__ = "dim_state"

    state_id: Mapped[str] = mapped_column(String(10), primary_key=True)  # e.g., 'IN-MH'
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    census_code: Mapped[Optional[str]] = mapped_column(String(10), unique=True)
    geom: Mapped[Optional[Geometry]] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=False),
        nullable=True
    )
    centroid: Mapped[Optional[Geometry]] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=False),
        nullable=True
    )

    districts: Mapped[List["DimDistrict"]] = relationship("DimDistrict", back_populates="state")

    __table_args__ = (
        Index("idx_dim_state_geom", "geom", postgresql_using="gist"),
        Index("idx_dim_state_centroid", "centroid", postgresql_using="gist"),
    )


class DimDistrict(Base, TimestampMixin):
    """District-level administrative spatial dimension."""
    __tablename__ = "dim_district"

    district_id: Mapped[str] = mapped_column(String(20), primary_key=True)  # e.g., 'IN-MH-PUN'
    state_id: Mapped[str] = mapped_column(String(10), ForeignKey("dim_state.state_id", ondelete="RESTRICT"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    census_code: Mapped[Optional[str]] = mapped_column(String(20))
    geom: Mapped[Optional[Geometry]] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=False),
        nullable=True
    )
    centroid: Mapped[Optional[Geometry]] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=False),
        nullable=True
    )

    state: Mapped["DimState"] = relationship("DimState", back_populates="districts")
    training_centers: Mapped[List["DimTrainingCenter"]] = relationship("DimTrainingCenter", back_populates="district")

    __table_args__ = (
        Index("idx_dim_district_state_name", "state_id", "name"),
        Index("idx_dim_district_geom", "geom", postgresql_using="gist"),
        Index("idx_dim_district_centroid", "centroid", postgresql_using="gist"),
    )


class DimSector(Base, TimestampMixin):
    """Economic / industry sector dimension."""
    __tablename__ = "dim_sector"

    sector_id: Mapped[str] = mapped_column(String(20), primary_key=True)  # e.g., 'SEC-AUTO'
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    ssc_code: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(Text)

    occupations: Mapped[List["DimOccupation"]] = relationship("DimOccupation", back_populates="sector")


class DimNco(Base):
    """Official National Classification of Occupations (NCO-2015) deterministic hierarchy."""
    __tablename__ = "dim_nco"

    nco_code: Mapped[str] = mapped_column(String(20), primary_key=True)  # e.g., '7231.0100'
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    division: Mapped[str] = mapped_column(String(2), nullable=False)       # 1-digit
    sub_division: Mapped[str] = mapped_column(String(4), nullable=False)   # 2-digit
    group_code: Mapped[str] = mapped_column(String(6), nullable=False)     # 3-digit
    family_code: Mapped[str] = mapped_column(String(8), nullable=False)    # 4-digit
    description: Mapped[Optional[str]] = mapped_column(Text)

    occupations: Mapped[List["DimOccupation"]] = relationship("DimOccupation", back_populates="nco")

    __table_args__ = (
        Index("idx_dim_nco_division", "division"),
        Index("idx_dim_nco_family", "family_code"),
    )


class DimOccupation(Base, TimestampMixin):
    """Canonical occupation entity mapped to official NCO and Sector."""
    __tablename__ = "dim_occupation"

    occupation_id: Mapped[str] = mapped_column(String(50), primary_key=True)  # e.g., 'OCC-7421-0300'
    nco_code: Mapped[str] = mapped_column(String(20), ForeignKey("dim_nco.nco_code", ondelete="RESTRICT"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    sector_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_sector.sector_id", ondelete="RESTRICT"), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)

    nco: Mapped["DimNco"] = relationship("DimNco", back_populates="occupations")
    sector: Mapped["DimSector"] = relationship("DimSector", back_populates="occupations")
    skill_links: Mapped[List["MapOccupationSkill"]] = relationship("MapOccupationSkill", back_populates="occupation")


class DimSkill(Base, TimestampMixin):
    """Canonical skill entity classified by domain type."""
    __tablename__ = "dim_skill"

    skill_id: Mapped[str] = mapped_column(String(50), primary_key=True)  # e.g., 'SKL-SOLAR-PV-INSTALL'
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    skill_type: Mapped[str] = mapped_column(String(30), default=SkillTypeEnum.TECHNICAL.value, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    occupation_links: Mapped[List["MapOccupationSkill"]] = relationship("MapOccupationSkill", back_populates="skill")
    qualification_links: Mapped[List["MapSkillQualification"]] = relationship("MapSkillQualification", back_populates="skill")

    __table_args__ = (
        Index("idx_dim_skill_type", "skill_type"),
    )


class DimNsqfLevel(Base):
    """National Skills Qualification Framework (NSQF 1 to 10) levels."""
    __tablename__ = "dim_nsqf_level"

    nsqf_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    descriptor: Mapped[str] = mapped_column(String(100), nullable=False)
    knowledge_competence: Mapped[Optional[str]] = mapped_column(Text)
    skill_competence: Mapped[Optional[str]] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint("nsqf_level >= 1 AND nsqf_level <= 10", name="chk_nsqf_level_range"),
    )


class DimQualification(Base, TimestampMixin):
    """Formal qualification or Qualification Pack (QP) aligned to NSQF and Sector."""
    __tablename__ = "dim_qualification"

    qualification_id: Mapped[str] = mapped_column(String(50), primary_key=True)  # e.g., 'QP-ASC-Q1402'
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    nsqf_level: Mapped[int] = mapped_column(Integer, ForeignKey("dim_nsqf_level.nsqf_level", ondelete="RESTRICT"), nullable=False, index=True)
    sector_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_sector.sector_id", ondelete="RESTRICT"), nullable=False, index=True)

    training_programs: Mapped[List["DimTrainingProgram"]] = relationship("DimTrainingProgram", back_populates="qualification")
    skill_links: Mapped[List["MapSkillQualification"]] = relationship("MapSkillQualification", back_populates="qualification")


class DimTrainingProgram(Base, TimestampMixin):
    """Accredited vocational or technical training curriculum."""
    __tablename__ = "dim_training_program"

    program_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    qualification_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_qualification.qualification_id", ondelete="RESTRICT"), nullable=False, index=True)
    duration_hours: Mapped[int] = mapped_column(Integer, default=300)
    curriculum_version: Mapped[str] = mapped_column(String(20), default="1.0")

    qualification: Mapped["DimQualification"] = relationship("DimQualification", back_populates="training_programs")


class DimTrainingCenter(Base, TimestampMixin):
    """Physical training provider / ITI / Kendra institution with GPS point location."""
    __tablename__ = "dim_training_center"

    center_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    district_id: Mapped[str] = mapped_column(String(20), ForeignKey("dim_district.district_id", ondelete="RESTRICT"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    center_type: Mapped[str] = mapped_column(String(50), default=CenterTypeEnum.ITI.value, nullable=False)
    is_accredited: Mapped[bool] = mapped_column(Boolean, default=True)
    geom: Mapped[Optional[Geometry]] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=False),
        nullable=True
    )

    district: Mapped["DimDistrict"] = relationship("DimDistrict", back_populates="training_centers")

    __table_args__ = (
        Index("idx_dim_training_center_type", "center_type"),
        Index("idx_dim_training_center_geom", "geom", postgresql_using="gist"),
    )


class DimSource(Base, TimestampMixin):
    """Catalogue of all registered data sources (official, survey, or fixture)."""
    __tablename__ = "dim_source"

    source_id: Mapped[str] = mapped_column(String(50), primary_key=True)  # e.g., 'SRC-NCS', 'SRC-FIXTURE-IND'
    authority: Mapped[str] = mapped_column(String(100), nullable=False)
    dataset_name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), default="1.0")
    retrieval_method: Mapped[str] = mapped_column(String(100), default="BATCH_IMPORT")
    coverage: Mapped[str] = mapped_column(String(100), default="NATIONAL")
    license: Mapped[str] = mapped_column(String(100), default="GOVERNMENT_OPEN_DATA")
    quality_score: Mapped[float] = mapped_column(Float, default=90.0)
    data_type: Mapped[str] = mapped_column(String(20), default=DataTypeEnum.REAL.value, nullable=False)

    __table_args__ = (
        CheckConstraint("quality_score >= 0.0 AND quality_score <= 100.0", name="chk_source_quality_range"),
    )


class MapOccupationSkill(Base):
    """Many-to-many relationship mapping Occupations to component Skills."""
    __tablename__ = "map_occupation_skill"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    occupation_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_occupation.occupation_id", ondelete="CASCADE"), nullable=False)
    skill_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_skill.skill_id", ondelete="CASCADE"), nullable=False)
    importance_weight: Mapped[float] = mapped_column(Float, default=1.0)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)

    occupation: Mapped["DimOccupation"] = relationship("DimOccupation", back_populates="skill_links")
    skill: Mapped["DimSkill"] = relationship("DimSkill", back_populates="occupation_links")

    __table_args__ = (
        Index("idx_map_occ_skill_unique", "occupation_id", "skill_id", unique=True),
        CheckConstraint("importance_weight >= 0.0 AND importance_weight <= 1.0", name="chk_occ_skill_weight_range"),
    )


class MapSkillQualification(Base):
    """Many-to-many relationship mapping Skills to formal Qualifications."""
    __tablename__ = "map_skill_qualification"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    skill_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_skill.skill_id", ondelete="CASCADE"), nullable=False)
    qualification_id: Mapped[str] = mapped_column(String(50), ForeignKey("dim_qualification.qualification_id", ondelete="CASCADE"), nullable=False)
    coverage_weight: Mapped[float] = mapped_column(Float, default=1.0)

    skill: Mapped["DimSkill"] = relationship("DimSkill", back_populates="qualification_links")
    qualification: Mapped["DimQualification"] = relationship("DimQualification", back_populates="skill_links")

    __table_args__ = (
        Index("idx_map_skill_qual_unique", "skill_id", "qualification_id", unique=True),
    )
