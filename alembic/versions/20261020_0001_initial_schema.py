"""Initial schema migration: PostGIS, pgcrypto, dimensions, facts, analytics, scenarios, governance.

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-10-20 23:55:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import geoalchemy2

revision: str = '0001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Enable required PostgreSQL extensions
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
    op.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto;')

    # Table: audit_log
    op.create_table('audit_log',
sa.Column('log_id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('user_id', sa.UUID(), nullable=True),
sa.Column('action', sa.String(length=100), nullable=False),
sa.Column('resource', sa.String(length=100), nullable=True),
sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
sa.Column('ip_address', sa.String(length=45), nullable=True),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.PrimaryKeyConstraint('log_id')
)

    op.create_index(op.f('ix_audit_log_user_id'), 'audit_log', ['user_id'], unique=False)

    op.create_index(op.f('ix_audit_log_action'), 'audit_log', ['action'], unique=False)

    # Table: dim_date
    op.create_table('dim_date',
sa.Column('date_key', sa.Date(), nullable=False),
sa.Column('day', sa.Integer(), nullable=False),
sa.Column('month', sa.Integer(), nullable=False),
sa.Column('quarter', sa.Integer(), nullable=False),
sa.Column('year', sa.Integer(), nullable=False),
sa.Column('financial_year', sa.String(length=10), nullable=False),
sa.Column('financial_quarter', sa.String(length=10), nullable=False),
sa.Column('month_name', sa.String(length=20), nullable=False),
sa.Column('is_weekend', sa.Boolean(), nullable=False),
sa.PrimaryKeyConstraint('date_key')
)

    op.create_index('idx_dim_date_year_month', 'dim_date', ['year', 'month'], unique=False)

    op.create_index('idx_dim_date_quarter', 'dim_date', ['quarter', 'year'], unique=False)

    # Table: dim_nco
    op.create_table('dim_nco',
sa.Column('nco_code', sa.String(length=20), nullable=False),
sa.Column('title', sa.String(length=255), nullable=False),
sa.Column('division', sa.String(length=2), nullable=False),
sa.Column('sub_division', sa.String(length=4), nullable=False),
sa.Column('group_code', sa.String(length=6), nullable=False),
sa.Column('family_code', sa.String(length=8), nullable=False),
sa.Column('description', sa.Text(), nullable=True),
sa.PrimaryKeyConstraint('nco_code')
)

    op.create_index('idx_dim_nco_family', 'dim_nco', ['family_code'], unique=False)

    op.create_index('idx_dim_nco_division', 'dim_nco', ['division'], unique=False)

    # Table: dim_nsqf_level
    op.create_table('dim_nsqf_level',
sa.Column('nsqf_level', sa.Integer(), nullable=False),
sa.Column('descriptor', sa.String(length=100), nullable=False),
sa.Column('knowledge_competence', sa.Text(), nullable=True),
sa.Column('skill_competence', sa.Text(), nullable=True),
sa.CheckConstraint('nsqf_level >= 1 AND nsqf_level <= 10', name='chk_nsqf_level_range'),
sa.PrimaryKeyConstraint('nsqf_level')
)

    # Table: dim_sector
    op.create_table('dim_sector',
sa.Column('sector_id', sa.String(length=20), nullable=False),
sa.Column('name', sa.String(length=100), nullable=False),
sa.Column('ssc_code', sa.String(length=50), nullable=True),
sa.Column('description', sa.Text(), nullable=True),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.PrimaryKeyConstraint('sector_id'),
sa.UniqueConstraint('name')
)

    # Table: dim_skill
    op.create_table('dim_skill',
sa.Column('skill_id', sa.String(length=50), nullable=False),
sa.Column('name', sa.String(length=255), nullable=False),
sa.Column('skill_type', sa.String(length=30), nullable=False),
sa.Column('description', sa.Text(), nullable=True),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.PrimaryKeyConstraint('skill_id'),
sa.UniqueConstraint('name')
)

    op.create_index('idx_dim_skill_type', 'dim_skill', ['skill_type'], unique=False)

    # Table: dim_source
    op.create_table('dim_source',
sa.Column('source_id', sa.String(length=50), nullable=False),
sa.Column('authority', sa.String(length=100), nullable=False),
sa.Column('dataset_name', sa.String(length=255), nullable=False),
sa.Column('version', sa.String(length=50), nullable=False),
sa.Column('retrieval_method', sa.String(length=100), nullable=False),
sa.Column('coverage', sa.String(length=100), nullable=False),
sa.Column('license', sa.String(length=100), nullable=False),
sa.Column('quality_score', sa.Float(), nullable=False),
sa.Column('data_type', sa.String(length=20), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('quality_score >= 0.0 AND quality_score <= 100.0', name='chk_source_quality_range'),
sa.PrimaryKeyConstraint('source_id')
)

    # Table: dim_state
    op.create_table('dim_state',
sa.Column('state_id', sa.String(length=10), nullable=False),
sa.Column('name', sa.String(length=100), nullable=False),
sa.Column('census_code', sa.String(length=10), nullable=True),
sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON', srid=4326, dimension=2, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
sa.Column('centroid', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, dimension=2, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.PrimaryKeyConstraint('state_id'),
sa.UniqueConstraint('census_code'),
sa.UniqueConstraint('name')
)

    op.create_index('idx_dim_state_geom', 'dim_state', ['geom'], unique=False, postgresql_using='gist')

    op.create_index('idx_dim_state_centroid', 'dim_state', ['centroid'], unique=False, postgresql_using='gist')

    # Table: forecast_run
    op.create_table('forecast_run',
sa.Column('run_id', sa.UUID(), nullable=False),
sa.Column('model_id', sa.String(length=50), nullable=False),
sa.Column('run_timestamp', sa.DateTime(timezone=True), nullable=False),
sa.Column('status', sa.String(length=30), nullable=False),
sa.Column('execution_time_ms', sa.Integer(), nullable=False),
sa.Column('parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
sa.Column('notes', sa.Text(), nullable=True),
sa.PrimaryKeyConstraint('run_id')
)

    op.create_index(op.f('ix_forecast_run_model_id'), 'forecast_run', ['model_id'], unique=False)

    # Table: model_registry
    op.create_table('model_registry',
sa.Column('model_id', sa.String(length=50), nullable=False),
sa.Column('model_type', sa.String(length=50), nullable=False),
sa.Column('algorithm_name', sa.String(length=100), nullable=False),
sa.Column('version', sa.String(length=50), nullable=False),
sa.Column('status', sa.String(length=20), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.PrimaryKeyConstraint('model_id')
)

    op.create_index(op.f('ix_model_registry_status'), 'model_registry', ['status'], unique=False)

    # Table: scenario
    op.create_table('scenario',
sa.Column('scenario_id', sa.UUID(), nullable=False),
sa.Column('user_id', sa.UUID(), nullable=True),
sa.Column('title', sa.String(length=255), nullable=False),
sa.Column('description', sa.Text(), nullable=True),
sa.Column('parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.PrimaryKeyConstraint('scenario_id')
)

    # Table: dataset_registry
    op.create_table('dataset_registry',
sa.Column('dataset_id', sa.String(length=50), nullable=False),
sa.Column('source_id', sa.String(length=50), nullable=False),
sa.Column('version', sa.String(length=50), nullable=False),
sa.Column('coverage_start', sa.Date(), nullable=True),
sa.Column('coverage_end', sa.Date(), nullable=True),
sa.Column('row_count', sa.BigInteger(), nullable=False),
sa.Column('data_type', sa.String(length=20), nullable=False),
sa.Column('status', sa.String(length=20), nullable=False),
sa.Column('quality_score', sa.Float(), nullable=False),
sa.Column('registered_at', sa.DateTime(timezone=True), nullable=False),
sa.ForeignKeyConstraint(['source_id'], ['dim_source.source_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('dataset_id')
)

    op.create_index(op.f('ix_dataset_registry_source_id'), 'dataset_registry', ['source_id'], unique=False)

    # Table: dim_district
    op.create_table('dim_district',
sa.Column('district_id', sa.String(length=20), nullable=False),
sa.Column('state_id', sa.String(length=10), nullable=False),
sa.Column('name', sa.String(length=100), nullable=False),
sa.Column('census_code', sa.String(length=20), nullable=True),
sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON', srid=4326, dimension=2, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
sa.Column('centroid', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, dimension=2, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.ForeignKeyConstraint(['state_id'], ['dim_state.state_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('district_id')
)

    op.create_index('idx_dim_district_state_name', 'dim_district', ['state_id', 'name'], unique=False)

    op.create_index('idx_dim_district_centroid', 'dim_district', ['centroid'], unique=False, postgresql_using='gist')

    op.create_index(op.f('ix_dim_district_state_id'), 'dim_district', ['state_id'], unique=False)

    op.create_index('idx_dim_district_geom', 'dim_district', ['geom'], unique=False, postgresql_using='gist')

    # Table: dim_occupation
    op.create_table('dim_occupation',
sa.Column('occupation_id', sa.String(length=50), nullable=False),
sa.Column('nco_code', sa.String(length=20), nullable=False),
sa.Column('title', sa.String(length=255), nullable=False),
sa.Column('sector_id', sa.String(length=20), nullable=False),
sa.Column('description', sa.Text(), nullable=True),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.ForeignKeyConstraint(['nco_code'], ['dim_nco.nco_code'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['sector_id'], ['dim_sector.sector_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('occupation_id')
)

    op.create_index(op.f('ix_dim_occupation_sector_id'), 'dim_occupation', ['sector_id'], unique=False)

    op.create_index(op.f('ix_dim_occupation_nco_code'), 'dim_occupation', ['nco_code'], unique=False)

    # Table: dim_qualification
    op.create_table('dim_qualification',
sa.Column('qualification_id', sa.String(length=50), nullable=False),
sa.Column('title', sa.String(length=255), nullable=False),
sa.Column('nsqf_level', sa.Integer(), nullable=False),
sa.Column('sector_id', sa.String(length=20), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.ForeignKeyConstraint(['nsqf_level'], ['dim_nsqf_level.nsqf_level'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['sector_id'], ['dim_sector.sector_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('qualification_id')
)

    op.create_index(op.f('ix_dim_qualification_sector_id'), 'dim_qualification', ['sector_id'], unique=False)

    op.create_index(op.f('ix_dim_qualification_nsqf_level'), 'dim_qualification', ['nsqf_level'], unique=False)

    # Table: model_run
    op.create_table('model_run',
sa.Column('run_id', sa.UUID(), nullable=False),
sa.Column('model_id', sa.String(length=50), nullable=False),
sa.Column('training_dataset_version', sa.String(length=50), nullable=False),
sa.Column('hyperparameters', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
sa.Column('train_start', sa.Date(), nullable=False),
sa.Column('train_end', sa.Date(), nullable=False),
sa.Column('val_start', sa.Date(), nullable=False),
sa.Column('val_end', sa.Date(), nullable=False),
sa.Column('metrics', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.ForeignKeyConstraint(['model_id'], ['model_registry.model_id'], ondelete='CASCADE'),
sa.PrimaryKeyConstraint('run_id')
)

    op.create_index(op.f('ix_model_run_model_id'), 'model_run', ['model_id'], unique=False)

    # Table: optimization_run
    op.create_table('optimization_run',
sa.Column('run_id', sa.UUID(), nullable=False),
sa.Column('user_id', sa.UUID(), nullable=True),
sa.Column('state_id', sa.String(length=10), nullable=False),
sa.Column('horizon_months', sa.Integer(), nullable=False),
sa.Column('budget_inr', sa.Numeric(precision=15, scale=2), nullable=False),
sa.Column('solver_status', sa.String(length=50), nullable=False),
sa.Column('objective_value', sa.Numeric(precision=15, scale=2), nullable=True),
sa.Column('allocated_budget_inr', sa.Numeric(precision=15, scale=2), nullable=True),
sa.Column('solve_time_ms', sa.Integer(), nullable=False),
sa.Column('parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('budget_inr >= 0', name='chk_opt_budget_non_neg'),
sa.ForeignKeyConstraint(['state_id'], ['dim_state.state_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('run_id')
)

    op.create_index(op.f('ix_optimization_run_state_id'), 'optimization_run', ['state_id'], unique=False)

    # Table: scenario_result
    op.create_table('scenario_result',
sa.Column('result_id', sa.UUID(), nullable=False),
sa.Column('scenario_id', sa.UUID(), nullable=False),
sa.Column('baseline_gap', sa.Numeric(precision=12, scale=2), nullable=False),
sa.Column('simulated_gap', sa.Numeric(precision=12, scale=2), nullable=False),
sa.Column('net_reduction', sa.Numeric(precision=12, scale=2), nullable=False),
sa.Column('reduction_pct', sa.Float(), nullable=False),
sa.Column('estimated_cost_inr', sa.Numeric(precision=15, scale=2), nullable=False),
sa.Column('confidence_score', sa.Float(), nullable=False),
sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.ForeignKeyConstraint(['scenario_id'], ['scenario.scenario_id'], ondelete='CASCADE'),
sa.PrimaryKeyConstraint('result_id')
)

    op.create_index(op.f('ix_scenario_result_scenario_id'), 'scenario_result', ['scenario_id'], unique=False)

    # Table: data_lineage
    op.create_table('data_lineage',
sa.Column('lineage_id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('target_entity_type', sa.String(length=50), nullable=False),
sa.Column('target_entity_id', sa.String(length=100), nullable=False),
sa.Column('source_dataset_id', sa.String(length=50), nullable=False),
sa.Column('transformation_pipeline', sa.String(length=100), nullable=False),
sa.Column('model_run_id', sa.UUID(), nullable=True),
sa.Column('recorded_at', sa.DateTime(timezone=True), nullable=False),
sa.ForeignKeyConstraint(['source_dataset_id'], ['dataset_registry.dataset_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('lineage_id')
)

    op.create_index(op.f('ix_data_lineage_source_dataset_id'), 'data_lineage', ['source_dataset_id'], unique=False)

    op.create_index(op.f('ix_data_lineage_target_entity_id'), 'data_lineage', ['target_entity_id'], unique=False)

    # Table: data_quality
    op.create_table('data_quality',
sa.Column('check_id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('dataset_id', sa.String(length=50), nullable=False),
sa.Column('check_name', sa.String(length=100), nullable=False),
sa.Column('completeness_pct', sa.Float(), nullable=False),
sa.Column('valid_geometry_pct', sa.Float(), nullable=False),
sa.Column('unmapped_nco_pct', sa.Float(), nullable=False),
sa.Column('duplicate_count', sa.Integer(), nullable=False),
sa.Column('passed', sa.Boolean(), nullable=False),
sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
sa.Column('checked_at', sa.DateTime(timezone=True), nullable=False),
sa.ForeignKeyConstraint(['dataset_id'], ['dataset_registry.dataset_id'], ondelete='CASCADE'),
sa.PrimaryKeyConstraint('check_id')
)

    op.create_index(op.f('ix_data_quality_dataset_id'), 'data_quality', ['dataset_id'], unique=False)

    # Table: dim_training_center
    op.create_table('dim_training_center',
sa.Column('center_id', sa.String(length=50), nullable=False),
sa.Column('district_id', sa.String(length=20), nullable=False),
sa.Column('name', sa.String(length=255), nullable=False),
sa.Column('center_type', sa.String(length=50), nullable=False),
sa.Column('is_accredited', sa.Boolean(), nullable=False),
sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, dimension=2, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.ForeignKeyConstraint(['district_id'], ['dim_district.district_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('center_id')
)

    op.create_index('idx_dim_training_center_geom', 'dim_training_center', ['geom'], unique=False, postgresql_using='gist')

    op.create_index(op.f('ix_dim_training_center_district_id'), 'dim_training_center', ['district_id'], unique=False)

    op.create_index('idx_dim_training_center_type', 'dim_training_center', ['center_type'], unique=False)

    # Table: dim_training_program
    op.create_table('dim_training_program',
sa.Column('program_id', sa.String(length=50), nullable=False),
sa.Column('qualification_id', sa.String(length=50), nullable=False),
sa.Column('duration_hours', sa.Integer(), nullable=False),
sa.Column('curriculum_version', sa.String(length=20), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.ForeignKeyConstraint(['qualification_id'], ['dim_qualification.qualification_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('program_id')
)

    op.create_index(op.f('ix_dim_training_program_qualification_id'), 'dim_training_program', ['qualification_id'], unique=False)

    # Table: fact_employer_signal
    op.create_table('fact_employer_signal',
sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('date_key', sa.Date(), nullable=False),
sa.Column('district_id', sa.String(length=20), nullable=False),
sa.Column('sector_id', sa.String(length=20), nullable=False),
sa.Column('active_employers_count', sa.Integer(), nullable=False),
sa.Column('hiring_expansion_sentiment', sa.Float(), nullable=False),
sa.Column('source_id', sa.String(length=50), nullable=False),
sa.Column('dataset_type', sa.String(length=20), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('active_employers_count >= 0', name='chk_employer_signal_count_non_neg'),
sa.ForeignKeyConstraint(['date_key'], ['dim_date.date_key'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['district_id'], ['dim_district.district_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['sector_id'], ['dim_sector.sector_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['source_id'], ['dim_source.source_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index(op.f('ix_fact_employer_signal_district_id'), 'fact_employer_signal', ['district_id'], unique=False)

    op.create_index(op.f('ix_fact_employer_signal_date_key'), 'fact_employer_signal', ['date_key'], unique=False)

    op.create_index('idx_fact_employer_geo_date', 'fact_employer_signal', ['district_id', 'sector_id', 'date_key'], unique=True)

    op.create_index(op.f('ix_fact_employer_signal_sector_id'), 'fact_employer_signal', ['sector_id'], unique=False)

    # Table: fact_job_demand
    op.create_table('fact_job_demand',
sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('date_key', sa.Date(), nullable=False),
sa.Column('district_id', sa.String(length=20), nullable=False),
sa.Column('occupation_id', sa.String(length=50), nullable=False),
sa.Column('active_postings', sa.Integer(), nullable=False),
sa.Column('new_postings', sa.Integer(), nullable=False),
sa.Column('median_days_open', sa.Integer(), nullable=False),
sa.Column('unique_employers', sa.Integer(), nullable=False),
sa.Column('source_id', sa.String(length=50), nullable=False),
sa.Column('dataset_type', sa.String(length=20), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('active_postings >= 0', name='chk_demand_active_postings_non_neg'),
sa.CheckConstraint('new_postings >= 0', name='chk_demand_new_postings_non_neg'),
sa.CheckConstraint('unique_employers >= 0', name='chk_demand_employers_non_neg'),
sa.ForeignKeyConstraint(['date_key'], ['dim_date.date_key'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['district_id'], ['dim_district.district_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['occupation_id'], ['dim_occupation.occupation_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['source_id'], ['dim_source.source_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index('idx_fact_demand_geo_occ_date', 'fact_job_demand', ['district_id', 'occupation_id', 'date_key'], unique=True)

    op.create_index(op.f('ix_fact_job_demand_occupation_id'), 'fact_job_demand', ['occupation_id'], unique=False)

    op.create_index(op.f('ix_fact_job_demand_date_key'), 'fact_job_demand', ['date_key'], unique=False)

    op.create_index(op.f('ix_fact_job_demand_district_id'), 'fact_job_demand', ['district_id'], unique=False)

    # Table: fact_skill_signal
    op.create_table('fact_skill_signal',
sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('date_key', sa.Date(), nullable=False),
sa.Column('district_id', sa.String(length=20), nullable=False),
sa.Column('skill_id', sa.String(length=50), nullable=False),
sa.Column('frequency_count', sa.Integer(), nullable=False),
sa.Column('growth_rate_mom', sa.Float(), nullable=False),
sa.Column('intensity_score', sa.Float(), nullable=False),
sa.Column('source_id', sa.String(length=50), nullable=False),
sa.Column('dataset_type', sa.String(length=20), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('frequency_count >= 0', name='chk_skill_signal_frequency_non_neg'),
sa.ForeignKeyConstraint(['date_key'], ['dim_date.date_key'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['district_id'], ['dim_district.district_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['skill_id'], ['dim_skill.skill_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['source_id'], ['dim_source.source_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index(op.f('ix_fact_skill_signal_date_key'), 'fact_skill_signal', ['date_key'], unique=False)

    op.create_index('idx_fact_skill_geo_date', 'fact_skill_signal', ['district_id', 'skill_id', 'date_key'], unique=True)

    op.create_index(op.f('ix_fact_skill_signal_district_id'), 'fact_skill_signal', ['district_id'], unique=False)

    op.create_index(op.f('ix_fact_skill_signal_skill_id'), 'fact_skill_signal', ['skill_id'], unique=False)

    # Table: fact_workforce_supply
    op.create_table('fact_workforce_supply',
sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('date_key', sa.Date(), nullable=False),
sa.Column('district_id', sa.String(length=20), nullable=False),
sa.Column('occupation_id', sa.String(length=50), nullable=False),
sa.Column('employed_stock', sa.Integer(), nullable=False),
sa.Column('unemployed_seeking', sa.Integer(), nullable=False),
sa.Column('fresh_graduates', sa.Integer(), nullable=False),
sa.Column('source_id', sa.String(length=50), nullable=False),
sa.Column('dataset_type', sa.String(length=20), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('employed_stock >= 0', name='chk_supply_employed_stock_non_neg'),
sa.CheckConstraint('unemployed_seeking >= 0', name='chk_supply_unemployed_non_neg'),
sa.ForeignKeyConstraint(['date_key'], ['dim_date.date_key'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['district_id'], ['dim_district.district_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['occupation_id'], ['dim_occupation.occupation_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['source_id'], ['dim_source.source_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index(op.f('ix_fact_workforce_supply_occupation_id'), 'fact_workforce_supply', ['occupation_id'], unique=False)

    op.create_index(op.f('ix_fact_workforce_supply_district_id'), 'fact_workforce_supply', ['district_id'], unique=False)

    op.create_index(op.f('ix_fact_workforce_supply_date_key'), 'fact_workforce_supply', ['date_key'], unique=False)

    op.create_index('idx_fact_supply_geo_occ_date', 'fact_workforce_supply', ['district_id', 'occupation_id', 'date_key'], unique=True)

    # Table: forecast_demand
    op.create_table('forecast_demand',
sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('run_id', sa.UUID(), nullable=False),
sa.Column('district_id', sa.String(length=20), nullable=False),
sa.Column('occupation_id', sa.String(length=50), nullable=False),
sa.Column('forecast_date', sa.Date(), nullable=False),
sa.Column('horizon_months', sa.Integer(), nullable=False),
sa.Column('point_estimate', sa.Float(), nullable=False),
sa.Column('lower_bound_80', sa.Float(), nullable=False),
sa.Column('upper_bound_80', sa.Float(), nullable=False),
sa.Column('lower_bound_95', sa.Float(), nullable=False),
sa.Column('upper_bound_95', sa.Float(), nullable=False),
sa.Column('model_name', sa.String(length=50), nullable=False),
sa.Column('is_champion', sa.Boolean(), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('horizon_months IN (3, 6, 12, 18, 24)', name='chk_demand_forecast_horizon_valid'),
sa.CheckConstraint('point_estimate >= 0', name='chk_demand_forecast_non_neg'),
sa.ForeignKeyConstraint(['district_id'], ['dim_district.district_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['occupation_id'], ['dim_occupation.occupation_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['run_id'], ['forecast_run.run_id'], ondelete='CASCADE'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index(op.f('ix_forecast_demand_occupation_id'), 'forecast_demand', ['occupation_id'], unique=False)

    op.create_index(op.f('ix_forecast_demand_run_id'), 'forecast_demand', ['run_id'], unique=False)

    op.create_index(op.f('ix_forecast_demand_district_id'), 'forecast_demand', ['district_id'], unique=False)

    op.create_index('idx_forecast_demand_lookup', 'forecast_demand', ['district_id', 'occupation_id', 'horizon_months', 'is_champion'], unique=False)

    # Table: forecast_supply
    op.create_table('forecast_supply',
sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('run_id', sa.UUID(), nullable=False),
sa.Column('district_id', sa.String(length=20), nullable=False),
sa.Column('occupation_id', sa.String(length=50), nullable=False),
sa.Column('forecast_date', sa.Date(), nullable=False),
sa.Column('horizon_months', sa.Integer(), nullable=False),
sa.Column('point_estimate', sa.Float(), nullable=False),
sa.Column('lower_bound_80', sa.Float(), nullable=False),
sa.Column('upper_bound_80', sa.Float(), nullable=False),
sa.Column('lower_bound_95', sa.Float(), nullable=False),
sa.Column('upper_bound_95', sa.Float(), nullable=False),
sa.Column('model_name', sa.String(length=50), nullable=False),
sa.Column('is_champion', sa.Boolean(), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('horizon_months IN (3, 6, 12, 18, 24)', name='chk_supply_forecast_horizon_valid'),
sa.CheckConstraint('point_estimate >= 0', name='chk_supply_forecast_non_neg'),
sa.ForeignKeyConstraint(['district_id'], ['dim_district.district_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['occupation_id'], ['dim_occupation.occupation_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['run_id'], ['forecast_run.run_id'], ondelete='CASCADE'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index(op.f('ix_forecast_supply_run_id'), 'forecast_supply', ['run_id'], unique=False)

    op.create_index('idx_forecast_supply_lookup', 'forecast_supply', ['district_id', 'occupation_id', 'horizon_months', 'is_champion'], unique=False)

    op.create_index(op.f('ix_forecast_supply_district_id'), 'forecast_supply', ['district_id'], unique=False)

    op.create_index(op.f('ix_forecast_supply_occupation_id'), 'forecast_supply', ['occupation_id'], unique=False)

    # Table: map_occupation_skill
    op.create_table('map_occupation_skill',
sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
sa.Column('occupation_id', sa.String(length=50), nullable=False),
sa.Column('skill_id', sa.String(length=50), nullable=False),
sa.Column('importance_weight', sa.Float(), nullable=False),
sa.Column('is_mandatory', sa.Boolean(), nullable=False),
sa.CheckConstraint('importance_weight >= 0.0 AND importance_weight <= 1.0', name='chk_occ_skill_weight_range'),
sa.ForeignKeyConstraint(['occupation_id'], ['dim_occupation.occupation_id'], ondelete='CASCADE'),
sa.ForeignKeyConstraint(['skill_id'], ['dim_skill.skill_id'], ondelete='CASCADE'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index('idx_map_occ_skill_unique', 'map_occupation_skill', ['occupation_id', 'skill_id'], unique=True)

    # Table: map_skill_qualification
    op.create_table('map_skill_qualification',
sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
sa.Column('skill_id', sa.String(length=50), nullable=False),
sa.Column('qualification_id', sa.String(length=50), nullable=False),
sa.Column('coverage_weight', sa.Float(), nullable=False),
sa.ForeignKeyConstraint(['qualification_id'], ['dim_qualification.qualification_id'], ondelete='CASCADE'),
sa.ForeignKeyConstraint(['skill_id'], ['dim_skill.skill_id'], ondelete='CASCADE'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index('idx_map_skill_qual_unique', 'map_skill_qualification', ['skill_id', 'qualification_id'], unique=True)

    # Table: model_metric
    op.create_table('model_metric',
sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('run_id', sa.UUID(), nullable=False),
sa.Column('metric_name', sa.String(length=50), nullable=False),
sa.Column('metric_value', sa.Float(), nullable=False),
sa.Column('horizon_months', sa.Integer(), nullable=False),
sa.Column('slice_name', sa.String(length=50), nullable=False),
sa.ForeignKeyConstraint(['run_id'], ['model_run.run_id'], ondelete='CASCADE'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index(op.f('ix_model_metric_run_id'), 'model_metric', ['run_id'], unique=False)

    op.create_index('idx_model_metric_run_name_horizon', 'model_metric', ['run_id', 'metric_name', 'horizon_months'], unique=False)

    # Table: risk_alert
    op.create_table('risk_alert',
sa.Column('alert_id', sa.String(length=50), nullable=False),
sa.Column('district_id', sa.String(length=20), nullable=False),
sa.Column('occupation_id', sa.String(length=50), nullable=False),
sa.Column('risk_class', sa.String(length=20), nullable=False),
sa.Column('title', sa.String(length=255), nullable=False),
sa.Column('description', sa.Text(), nullable=False),
sa.Column('trigger_drivers', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
sa.Column('is_active', sa.Boolean(), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.ForeignKeyConstraint(['district_id'], ['dim_district.district_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['occupation_id'], ['dim_occupation.occupation_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('alert_id')
)

    op.create_index('idx_risk_alert_active_class', 'risk_alert', ['is_active', 'risk_class'], unique=False)

    op.create_index(op.f('ix_risk_alert_district_id'), 'risk_alert', ['district_id'], unique=False)

    op.create_index(op.f('ix_risk_alert_occupation_id'), 'risk_alert', ['occupation_id'], unique=False)

    op.create_index(op.f('ix_risk_alert_is_active'), 'risk_alert', ['is_active'], unique=False)

    op.create_index(op.f('ix_risk_alert_risk_class'), 'risk_alert', ['risk_class'], unique=False)

    # Table: skill_gap
    op.create_table('skill_gap',
sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('district_id', sa.String(length=20), nullable=False),
sa.Column('occupation_id', sa.String(length=50), nullable=False),
sa.Column('horizon_months', sa.Integer(), nullable=False),
sa.Column('demand_index', sa.Float(), nullable=False),
sa.Column('supply_index', sa.Float(), nullable=False),
sa.Column('projected_gap', sa.Numeric(precision=12, scale=2), nullable=False),
sa.Column('gap_growth_rate', sa.Float(), nullable=False),
sa.Column('confidence_score', sa.Float(), nullable=False),
sa.Column('model_agreement', sa.String(length=20), nullable=False),
sa.Column('risk_class', sa.String(length=20), nullable=False),
sa.Column('calculated_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('confidence_score >= 0.0 AND confidence_score <= 1.0', name='chk_gap_confidence_range'),
sa.CheckConstraint('demand_index >= 0.0 AND demand_index <= 100.0', name='chk_gap_demand_index_range'),
sa.CheckConstraint('supply_index >= 0.0 AND supply_index <= 100.0', name='chk_gap_supply_index_range'),
sa.ForeignKeyConstraint(['district_id'], ['dim_district.district_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['occupation_id'], ['dim_occupation.occupation_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index('idx_skill_gap_geo_occ_horizon', 'skill_gap', ['district_id', 'occupation_id', 'horizon_months'], unique=True)

    op.create_index(op.f('ix_skill_gap_district_id'), 'skill_gap', ['district_id'], unique=False)

    op.create_index(op.f('ix_skill_gap_occupation_id'), 'skill_gap', ['occupation_id'], unique=False)

    op.create_index(op.f('ix_skill_gap_risk_class'), 'skill_gap', ['risk_class'], unique=False)

    # Table: fact_training_capacity
    op.create_table('fact_training_capacity',
sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('date_key', sa.Date(), nullable=False),
sa.Column('center_id', sa.String(length=50), nullable=False),
sa.Column('qualification_id', sa.String(length=50), nullable=False),
sa.Column('sanctioned_seats', sa.Integer(), nullable=False),
sa.Column('enrolled_trainees', sa.Integer(), nullable=False),
sa.Column('source_id', sa.String(length=50), nullable=False),
sa.Column('dataset_type', sa.String(length=20), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('enrolled_trainees >= 0', name='chk_capacity_enrolled_non_neg'),
sa.CheckConstraint('sanctioned_seats >= 0', name='chk_capacity_seats_non_neg'),
sa.ForeignKeyConstraint(['center_id'], ['dim_training_center.center_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['date_key'], ['dim_date.date_key'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['qualification_id'], ['dim_qualification.qualification_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['source_id'], ['dim_source.source_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index(op.f('ix_fact_training_capacity_qualification_id'), 'fact_training_capacity', ['qualification_id'], unique=False)

    op.create_index(op.f('ix_fact_training_capacity_center_id'), 'fact_training_capacity', ['center_id'], unique=False)

    op.create_index(op.f('ix_fact_training_capacity_date_key'), 'fact_training_capacity', ['date_key'], unique=False)

    op.create_index('idx_fact_capacity_center_qual_date', 'fact_training_capacity', ['center_id', 'qualification_id', 'date_key'], unique=True)

    # Table: fact_training_outcomes
    op.create_table('fact_training_outcomes',
sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
sa.Column('date_key', sa.Date(), nullable=False),
sa.Column('center_id', sa.String(length=50), nullable=False),
sa.Column('qualification_id', sa.String(length=50), nullable=False),
sa.Column('completed_trainees', sa.Integer(), nullable=False),
sa.Column('certified_trainees', sa.Integer(), nullable=False),
sa.Column('placed_trainees', sa.Integer(), nullable=False),
sa.Column('source_id', sa.String(length=50), nullable=False),
sa.Column('dataset_type', sa.String(length=20), nullable=False),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('certified_trainees >= 0', name='chk_outcomes_certified_non_neg'),
sa.CheckConstraint('completed_trainees >= 0', name='chk_outcomes_completed_non_neg'),
sa.CheckConstraint('placed_trainees >= 0', name='chk_outcomes_placed_non_neg'),
sa.ForeignKeyConstraint(['center_id'], ['dim_training_center.center_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['date_key'], ['dim_date.date_key'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['qualification_id'], ['dim_qualification.qualification_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['source_id'], ['dim_source.source_id'], ondelete='RESTRICT'),
sa.PrimaryKeyConstraint('id')
)

    op.create_index(op.f('ix_fact_training_outcomes_qualification_id'), 'fact_training_outcomes', ['qualification_id'], unique=False)

    op.create_index('idx_fact_outcomes_center_qual_date', 'fact_training_outcomes', ['center_id', 'qualification_id', 'date_key'], unique=True)

    op.create_index(op.f('ix_fact_training_outcomes_center_id'), 'fact_training_outcomes', ['center_id'], unique=False)

    op.create_index(op.f('ix_fact_training_outcomes_date_key'), 'fact_training_outcomes', ['date_key'], unique=False)

    # Table: optimization_result
    op.create_table('optimization_result',
sa.Column('result_id', sa.UUID(), nullable=False),
sa.Column('run_id', sa.UUID(), nullable=False),
sa.Column('rank', sa.Integer(), nullable=False),
sa.Column('center_id', sa.String(length=50), nullable=False),
sa.Column('qualification_id', sa.String(length=50), nullable=False),
sa.Column('action', sa.String(length=50), nullable=False),
sa.Column('seat_delta', sa.Integer(), nullable=False),
sa.Column('cost_inr', sa.Numeric(precision=15, scale=2), nullable=False),
sa.Column('expected_gap_reduction', sa.Numeric(precision=12, scale=2), nullable=False),
sa.Column('rationale', sa.Text(), nullable=True),
sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
sa.CheckConstraint('cost_inr >= 0', name='chk_opt_result_cost_non_neg'),
sa.CheckConstraint('seat_delta >= 0', name='chk_opt_result_seat_delta_non_neg'),
sa.ForeignKeyConstraint(['center_id'], ['dim_training_center.center_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['qualification_id'], ['dim_qualification.qualification_id'], ondelete='RESTRICT'),
sa.ForeignKeyConstraint(['run_id'], ['optimization_run.run_id'], ondelete='CASCADE'),
sa.PrimaryKeyConstraint('result_id')
)

    op.create_index(op.f('ix_optimization_result_run_id'), 'optimization_result', ['run_id'], unique=False)

    op.create_index('idx_opt_result_run_rank', 'optimization_result', ['run_id', 'rank'], unique=False)


def downgrade() -> None:
    op.drop_table('optimization_result')
    op.drop_table('fact_training_outcomes')
    op.drop_table('fact_training_capacity')
    op.drop_table('skill_gap')
    op.drop_table('risk_alert')
    op.drop_table('model_metric')
    op.drop_table('map_skill_qualification')
    op.drop_table('map_occupation_skill')
    op.drop_table('forecast_supply')
    op.drop_table('forecast_demand')
    op.drop_table('fact_workforce_supply')
    op.drop_table('fact_skill_signal')
    op.drop_table('fact_job_demand')
    op.drop_table('fact_employer_signal')
    op.drop_table('dim_training_program')
    op.drop_table('dim_training_center')
    op.drop_table('data_quality')
    op.drop_table('data_lineage')
    op.drop_table('scenario_result')
    op.drop_table('optimization_run')
    op.drop_table('model_run')
    op.drop_table('dim_qualification')
    op.drop_table('dim_occupation')
    op.drop_table('dim_district')
    op.drop_table('dataset_registry')
    op.drop_table('scenario')
    op.drop_table('model_registry')
    op.drop_table('forecast_run')
    op.drop_table('dim_state')
    op.drop_table('dim_source')
    op.drop_table('dim_skill')
    op.drop_table('dim_sector')
    op.drop_table('dim_nsqf_level')
    op.drop_table('dim_nco')
    op.drop_table('dim_date')
    op.drop_table('audit_log')
    op.execute('DROP EXTENSION IF EXISTS pgcrypto;')
    op.execute('DROP EXTENSION IF EXISTS postgis;')
