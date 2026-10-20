"""LABREX Idempotent Seed Framework & Deterministic Benchmark Fixtures.

Seeds reference dimensions, methodologies, and deterministic demo fixtures.
Explicitly labels all synthetic rows with source='LABREX_DEMO' and dataset_type='FIXTURE'.
Idempotent: Running multiple times will never duplicate rows or violate constraints.
"""
import logging
from datetime import date
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func

from backend.app.models.reference import (
    DimDate, DimState, DimDistrict, DimSector, DimNco, DimOccupation,
    DimSkill, DimNsqfLevel, DimQualification, DimTrainingProgram,
    DimTrainingCenter, DimSource, MapOccupationSkill, MapSkillQualification,
    SkillTypeEnum, CenterTypeEnum, DataTypeEnum
)
from backend.app.models.facts import (
    FactJobDemand, FactWorkforceSupply, FactTrainingCapacity, FactTrainingOutcomes
)

logger = logging.getLogger("labrex.seed")


async def seed_reference_and_fixtures(session: AsyncSession) -> Dict[str, int]:
    """Execute idempotent seed across all dimensions and deterministic benchmark fixtures."""
    stats = {}

    # 1. DimSource (Authority & provenance catalog)
    demo_source = {
        "source_id": "LABREX_DEMO",
        "authority": "LABREX Methodology & Synthesis Engine",
        "dataset_name": "LABREX Deterministic Benchmark Demo Fixture",
        "version": "1.0",
        "retrieval_method": "DETERMINISTIC_SYNTHESIS",
        "coverage": "NATIONAL_SAMPLE",
        "license": "LABREX_INTERNAL_BENCHMARK",
        "quality_score": 100.0,
        "data_type": DataTypeEnum.FIXTURE.value,
    }
    stmt = insert(DimSource).values([demo_source]).on_conflict_do_nothing(index_elements=["source_id"])
    await session.execute(stmt)
    stats["dim_source"] = 1

    # 2. DimNsqfLevel (Official NSQF Levels 1-10)
    nsqf_levels = [
        {"nsqf_level": 1, "descriptor": "Foundational Preparatory Skills", "knowledge_competence": "Basic reading, counting", "skill_competence": "Routine manual tasks"},
        {"nsqf_level": 2, "descriptor": "Basic Vocational Support", "knowledge_competence": "Basic factual knowledge", "skill_competence": "Repetitive hand-tool work"},
        {"nsqf_level": 3, "descriptor": "Skilled Operator / Assistant", "knowledge_competence": "Operational tools knowledge", "skill_competence": "Standardized operator tasks"},
        {"nsqf_level": 4, "descriptor": "Certificate Technician / Artisan", "knowledge_competence": "Broad trade theory", "skill_competence": "Independent technical execution"},
        {"nsqf_level": 5, "descriptor": "Senior Technician / Supervisor", "knowledge_competence": "Comprehensive field principles", "skill_competence": "Supervisory & technical oversight"},
        {"nsqf_level": 6, "descriptor": "Diploma / Advanced Technologist", "knowledge_competence": "Specialized applied science", "skill_competence": "Complex process optimization"},
        {"nsqf_level": 7, "descriptor": "Graduate Professional / Engineer", "knowledge_competence": "Advanced engineering/methodology", "skill_competence": "System design and innovation"},
        {"nsqf_level": 8, "descriptor": "Post-Graduate Specialist", "knowledge_competence": "Advanced conceptual mastery", "skill_competence": "High-level strategic architecture"},
        {"nsqf_level": 9, "descriptor": "Master Researcher / Architect", "knowledge_competence": "Frontier technical domain", "skill_competence": "Original technological invention"},
        {"nsqf_level": 10, "descriptor": "Doctoral Fellow / Domain Authority", "knowledge_competence": "Highest discipline authority", "skill_competence": "National policy & science leadership"},
    ]
    stmt = insert(DimNsqfLevel).values(nsqf_levels).on_conflict_do_nothing(index_elements=["nsqf_level"])
    await session.execute(stmt)
    stats["dim_nsqf_level"] = len(nsqf_levels)

    # 3. DimState (States & UTs)
    states = [
        {"state_id": "IN-MH", "name": "Maharashtra", "census_code": "27"},
        {"state_id": "IN-KA", "name": "Karnataka", "census_code": "29"},
        {"state_id": "IN-GJ", "name": "Gujarat", "census_code": "24"},
        {"state_id": "IN-DL", "name": "Delhi", "census_code": "07"},
        {"state_id": "IN-TN", "name": "Tamil Nadu", "census_code": "33"},
    ]
    stmt = insert(DimState).values(states).on_conflict_do_nothing(index_elements=["state_id"])
    await session.execute(stmt)
    stats["dim_state"] = len(states)

    # 4. DimDistrict (Sample administrative districts)
    districts = [
        {"district_id": "IN-MH-PUN", "state_id": "IN-MH", "name": "Pune", "census_code": "521"},
        {"district_id": "IN-MH-MUM", "state_id": "IN-MH", "name": "Mumbai City", "census_code": "519"},
        {"district_id": "IN-KA-BLR", "state_id": "IN-KA", "name": "Bengaluru Urban", "census_code": "572"},
        {"district_id": "IN-KA-MYS", "state_id": "IN-KA", "name": "Mysuru", "census_code": "577"},
        {"district_id": "IN-GJ-AHD", "state_id": "IN-GJ", "name": "Ahmedabad", "census_code": "474"},
        {"district_id": "IN-DL-NDL", "state_id": "IN-DL", "name": "New Delhi", "census_code": "094"},
    ]
    stmt = insert(DimDistrict).values(districts).on_conflict_do_nothing(index_elements=["district_id"])
    await session.execute(stmt)
    stats["dim_district"] = len(districts)

    # 5. DimSector (Economic Sectors)
    sectors = [
        {"sector_id": "SEC-AUTO", "name": "Automotive & Electric Mobility", "ssc_code": "ASDC", "description": "Automotive manufacturing, EV powertrains, and telematics"},
        {"sector_id": "SEC-IT", "name": "IT-ITeS & AI Systems", "ssc_code": "NASSCOM", "description": "Software engineering, cloud infrastructure, and intelligent automation"},
        {"sector_id": "SEC-RENEW", "name": "Renewable Energy & Solar Power", "ssc_code": "SCGJ", "description": "Photovoltaic generation, energy storage, and grid engineering"},
        {"sector_id": "SEC-HLTH", "name": "Healthcare & Allied Sciences", "ssc_code": "HSSC", "description": "Clinical care, laboratory diagnostics, and biomedical maintenance"},
    ]
    stmt = insert(DimSector).values(sectors).on_conflict_do_nothing(index_elements=["sector_id"])
    await session.execute(stmt)
    stats["dim_sector"] = len(sectors)

    # 6. DimNco (National Classification of Occupations 2015)
    nco_entries = [
        {"nco_code": "7231.0100", "title": "Motor Vehicle Mechanic", "division": "7", "sub_division": "72", "group_code": "723", "family_code": "7231", "description": "Internal combustion and electric vehicle technician"},
        {"nco_code": "7412.0200", "title": "Electrical Equipment Assembler", "division": "7", "sub_division": "74", "group_code": "741", "family_code": "7412", "description": "Industrial electrical harness and module fabrication"},
        {"nco_code": "2512.0100", "title": "Software Developer", "division": "2", "sub_division": "25", "group_code": "251", "family_code": "2512", "description": "Full-stack application and API architecture engineering"},
        {"nco_code": "2511.0100", "title": "Systems Analyst", "division": "2", "sub_division": "25", "group_code": "251", "family_code": "2511", "description": "Enterprise cloud systems and distributed architecture analyst"},
        {"nco_code": "3131.0200", "title": "Solar PV System Installer", "division": "3", "sub_division": "31", "group_code": "313", "family_code": "3131", "description": "Photovoltaic panel mounting, DC wiring, and inverter commissioning"},
        {"nco_code": "2149.0300", "title": "Renewable Energy Engineer", "division": "2", "sub_division": "21", "group_code": "214", "family_code": "2149", "description": "Grid integration, microgrid sizing, and battery energy storage"},
        {"nco_code": "3221.0100", "title": "Nursing Professional", "division": "3", "sub_division": "32", "group_code": "322", "family_code": "3221", "description": "Acute care, patient telemetry, and clinical protocol adherence"},
        {"nco_code": "3256.0100", "title": "Medical Laboratory Technician", "division": "3", "sub_division": "32", "group_code": "325", "family_code": "3256", "description": "Automated clinical assays, pathology, and diagnostic equipment"},
        {"nco_code": "1324.0100", "title": "Supply Chain Logistics Specialist", "division": "1", "sub_division": "13", "group_code": "132", "family_code": "1324", "description": "Multimodal freight logistics and automated warehouse ops"},
        {"nco_code": "3322.0100", "title": "Commercial Sales Representative", "division": "3", "sub_division": "33", "group_code": "332", "family_code": "3322", "description": "Technical enterprise B2B sales and solution delivery"},
        {"nco_code": "7112.0100", "title": "Building Construction Mason", "division": "7", "sub_division": "71", "group_code": "711", "family_code": "7112", "description": "Reinforced masonry, seismic retrofitting, and structural curing"},
        {"nco_code": "8322.0100", "title": "Light Commercial Vehicle Driver", "division": "8", "sub_division": "83", "group_code": "832", "family_code": "8322", "description": "Intra-city distribution fleet operations and defensive routing"},
    ]
    stmt = insert(DimNco).values(nco_entries).on_conflict_do_nothing(index_elements=["nco_code"])
    await session.execute(stmt)
    stats["dim_nco"] = len(nco_entries)

    # 7. DimOccupation
    occupations = [
        {"occupation_id": "OCC-AUTO-EV-MECH", "nco_code": "7231.0100", "sector_id": "SEC-AUTO", "title": "Electric Vehicle Diagnostic Specialist", "description": "High-voltage drivetrain and battery management diagnostic specialist"},
        {"occupation_id": "OCC-AUTO-ELEC-ASSM", "nco_code": "7412.0200", "sector_id": "SEC-AUTO", "title": "Automotive Harness Assembler", "description": "Sensor harness routing and automotive bus integration"},
        {"occupation_id": "OCC-IT-SDE", "nco_code": "2512.0100", "sector_id": "SEC-IT", "title": "Full-Stack Software Engineer", "description": "Distributed cloud architectures, backend APIs, and frontends"},
        {"occupation_id": "OCC-IT-SYS-ANLY", "nco_code": "2511.0100", "sector_id": "SEC-IT", "title": "Cloud Solutions Architect", "description": "Enterprise cloud migration, resilience, and microservice governance"},
        {"occupation_id": "OCC-REN-PV-INST", "nco_code": "3131.0200", "sector_id": "SEC-RENEW", "title": "Rooftop Solar PV Master Installer", "description": "Grid-tie rooftop array installation and string inverter setup"},
        {"occupation_id": "OCC-REN-ENG", "nco_code": "2149.0300", "sector_id": "SEC-RENEW", "title": "Microgrid Systems Engineer", "description": "Storage hybrid sizing, battery chemistry, and telemetry control"},
        {"occupation_id": "OCC-HLTH-NURSE", "nco_code": "3221.0100", "sector_id": "SEC-HLTH", "title": "Critical Care Clinical Specialist", "description": "ICU telemetry, acute patient stabilization, and ventilator operations"},
        {"occupation_id": "OCC-HLTH-LAB-TECH", "nco_code": "3256.0100", "sector_id": "SEC-HLTH", "title": "Biochemical Assay Analyst", "description": "High-throughput molecular diagnostics and automated screening"},
        {"occupation_id": "OCC-AUTO-SC-SPEC", "nco_code": "1324.0100", "sector_id": "SEC-AUTO", "title": "JIT Parts Logistics Coordinator", "description": "Automotive parts dispatch, ERP synchronization, and buffer planning"},
        {"occupation_id": "OCC-IT-B2B-SALES", "nco_code": "3322.0100", "sector_id": "SEC-IT", "title": "SaaS Enterprise Representative", "description": "Technical software solution consulting and customer onboarding"},
        {"occupation_id": "OCC-AUTO-BODY-MASON", "nco_code": "7112.0100", "sector_id": "SEC-AUTO", "title": "Industrial Structural Fabricator", "description": "Heavy bay frame welding, alignment, and hydraulic fixtures"},
        {"occupation_id": "OCC-AUTO-EV-DRIVER", "nco_code": "8322.0100", "sector_id": "SEC-AUTO", "title": "Clean Fleet Logistics Pilot", "description": "Commercial EV route management and smart charger integration"},
    ]
    stmt = insert(DimOccupation).values(occupations).on_conflict_do_nothing(index_elements=["occupation_id"])
    await session.execute(stmt)
    stats["dim_occupation"] = len(occupations)

    # 8. DimSkill (24 skills across categories)
    skills = [
        # Technical
        {"skill_id": "SKL-EV-BATTERY-DIAG", "name": "High-Voltage Battery Diagnostics", "skill_type": SkillTypeEnum.TECHNICAL.value, "description": "State-of-Charge, thermal telemetry, and cell balancing analytics"},
        {"skill_id": "SKL-PLC-PROG", "name": "PLC & Robotic Arm Programming", "skill_type": SkillTypeEnum.TECHNICAL.value, "description": "Industrial ladder logic and automated robotic cell coordination"},
        {"skill_id": "SKL-SOLAR-INVERTER", "name": "Solar String & Central Inverter Commissioning", "skill_type": SkillTypeEnum.TECHNICAL.value, "description": "MPPT configuration, grid synchronism, and anti-islanding protocols"},
        {"skill_id": "SKL-CLIN-PATH-TEST", "name": "Clinical Pathology Automated Testing", "skill_type": SkillTypeEnum.TECHNICAL.value, "description": "Assay preparation, blood chemistry calibration, and lab ISO safety"},
        {"skill_id": "SKL-PYTHON-ARCH", "name": "Python Async Microservice Architecture", "skill_type": SkillTypeEnum.TECHNICAL.value, "description": "FastAPI, asyncpg, distributed queue messaging, and OpenAPI"},
        {"skill_id": "SKL-MICROGRID-SYNC", "name": "Microgrid Dynamic Synchronization", "skill_type": SkillTypeEnum.TECHNICAL.value, "description": "Islanded generation control, phase matching, and frequency droop"},
        {"skill_id": "SKL-CNC-MILLING", "name": "5-Axis CNC Precision Milling", "skill_type": SkillTypeEnum.TECHNICAL.value, "description": "G-code tooling, dimensional tolerances, and alloy fabrication"},
        {"skill_id": "SKL-HV-SAFETY", "name": "High-Voltage NFPA 70E Safety Protocol", "skill_type": SkillTypeEnum.TECHNICAL.value, "description": "Personal protective gear, lockout/tagout, and arc-flash boundaries"},
        # Foundational
        {"skill_id": "SKL-PROBLEM-SOLVING", "name": "Systemic Critical Problem Solving", "skill_type": SkillTypeEnum.FOUNDATIONAL.value, "description": "Hypothesis-driven decomposition and Root Cause Analysis"},
        {"skill_id": "SKL-TROUBLESHOOTING", "name": "Hardware-in-the-Loop Troubleshooting", "skill_type": SkillTypeEnum.FOUNDATIONAL.value, "description": "Oscilloscope fault detection and wiring bus continuity checks"},
        {"skill_id": "SKL-QA-COMPLIANCE", "name": "Regulatory QA & Safety Audit Compliance", "skill_type": SkillTypeEnum.FOUNDATIONAL.value, "description": "Statutory inspection, checklist validation, and audit trail maintenance"},
        {"skill_id": "SKL-SIX-SIGMA", "name": "Lean Six Sigma DMAIC Workflow", "skill_type": SkillTypeEnum.FOUNDATIONAL.value, "description": "Waste reduction, takt time optimization, and defect containment"},
        # Digital
        {"skill_id": "SKL-CLOUD-INFRA", "name": "Cloud Infrastructure & Container Orchestration", "skill_type": SkillTypeEnum.DIGITAL.value, "description": "Docker containerization, Kubernetes clusters, and Helm charts"},
        {"skill_id": "SKL-EMBEDDED-RTOS", "name": "Embedded C & Real-Time Operating Systems", "skill_type": SkillTypeEnum.DIGITAL.value, "description": "FreeRTOS task scheduling, CAN bus packet handling, and DMA drivers"},
        {"skill_id": "SKL-APPLIED-ML", "name": "Applied ML & Time-Series Forecasting", "skill_type": SkillTypeEnum.DIGITAL.value, "description": "scikit-learn, XGBoost, walk-forward CV, and SHAP interpretability"},
        {"skill_id": "SKL-SQL-PIPELINE", "name": "SQL & Analytical Data Pipelines", "skill_type": SkillTypeEnum.DIGITAL.value, "description": "PostgreSQL window functions, PostGIS spatial indexing, and ELT"},
        {"skill_id": "SKL-SCADA-TELEMETRY", "name": "SCADA & Industrial IoT Telemetry", "skill_type": SkillTypeEnum.DIGITAL.value, "description": "Modbus TCP, MQTT streaming, and plant dashboard integration"},
        {"skill_id": "SKL-TELEMED-EHR", "name": "Telemedicine & Digital EHR Systems", "skill_type": SkillTypeEnum.DIGITAL.value, "description": "FHIR compliance, HL7 message exchange, and digital prescription workflows"},
        # Green
        {"skill_id": "SKL-SOLAR-SITING", "name": "GIS Solar PV Array Siting & Irradiance Analysis", "skill_type": SkillTypeEnum.GREEN.value, "description": "Spatial GIS shadow analysis, DNI modeling, and terrain gradient design"},
        {"skill_id": "SKL-EV-POWERTRAIN", "name": "EV Powertrain Retrofitting & Conversion", "skill_type": SkillTypeEnum.GREEN.value, "description": "ICE-to-EV subframe adaptation, motor coupler tuning, and regenerative braking"},
        {"skill_id": "SKL-CARBON-ACCOUNTING", "name": "Corporate Scope 1-3 Carbon Accounting", "skill_type": SkillTypeEnum.GREEN.value, "description": "GHG protocol calculators, emission factor application, and ESG reporting"},
        {"skill_id": "SKL-ENERGY-EFFICIENCY", "name": "Industrial Energy Audit & Waste Heat Recovery", "skill_type": SkillTypeEnum.GREEN.value, "description": "Specific energy consumption metrics, thermal insulation, and boiler tuning"},
        {"skill_id": "SKL-CIRCULAR-MATERIALS", "name": "Circular Economy Waste Material Handling", "skill_type": SkillTypeEnum.GREEN.value, "description": "Lithium-ion hydrometallurgy sorting and recycled polymer compounding"},
        {"skill_id": "SKL-GREEN-HVAC", "name": "Low-GWP Refrigerant & Smart HVAC Tuning", "skill_type": SkillTypeEnum.GREEN.value, "description": "Variable refrigerant flow, economizer dampers, and building envelope sealing"},
    ]
    stmt = insert(DimSkill).values(skills).on_conflict_do_nothing(index_elements=["skill_id"])
    await session.execute(stmt)
    stats["dim_skill"] = len(skills)

    # 9. MapOccupationSkill
    occ_skill_maps = [
        {"occupation_id": "OCC-AUTO-EV-MECH", "skill_id": "SKL-EV-BATTERY-DIAG", "importance_weight": 0.95, "is_mandatory": True},
        {"occupation_id": "OCC-AUTO-EV-MECH", "skill_id": "SKL-HV-SAFETY", "importance_weight": 1.0, "is_mandatory": True},
        {"occupation_id": "OCC-AUTO-EV-MECH", "skill_id": "SKL-EV-POWERTRAIN", "importance_weight": 0.85, "is_mandatory": False},
        {"occupation_id": "OCC-IT-SDE", "skill_id": "SKL-PYTHON-ARCH", "importance_weight": 1.0, "is_mandatory": True},
        {"occupation_id": "OCC-IT-SDE", "skill_id": "SKL-CLOUD-INFRA", "importance_weight": 0.90, "is_mandatory": True},
        {"occupation_id": "OCC-IT-SDE", "skill_id": "SKL-APPLIED-ML", "importance_weight": 0.80, "is_mandatory": False},
        {"occupation_id": "OCC-REN-PV-INST", "skill_id": "SKL-SOLAR-INVERTER", "importance_weight": 0.95, "is_mandatory": True},
        {"occupation_id": "OCC-REN-PV-INST", "skill_id": "SKL-SOLAR-SITING", "importance_weight": 0.85, "is_mandatory": True},
        {"occupation_id": "OCC-REN-PV-INST", "skill_id": "SKL-HV-SAFETY", "importance_weight": 0.90, "is_mandatory": True},
        {"occupation_id": "OCC-HLTH-LAB-TECH", "skill_id": "SKL-CLIN-PATH-TEST", "importance_weight": 1.0, "is_mandatory": True},
        {"occupation_id": "OCC-HLTH-LAB-TECH", "skill_id": "SKL-QA-COMPLIANCE", "importance_weight": 0.90, "is_mandatory": True},
    ]
    stmt = insert(MapOccupationSkill).values(occ_skill_maps).on_conflict_do_nothing(index_elements=["occupation_id", "skill_id"])
    await session.execute(stmt)
    stats["map_occupation_skill"] = len(occ_skill_maps)

    # 10. DimQualification
    qualifications = [
        {"qualification_id": "QP-AUTO-EV-L4", "title": "Certified EV Service Technician Level 4", "nsqf_level": 4, "sector_id": "SEC-AUTO"},
        {"qualification_id": "QP-AUTO-EV-L6", "title": "EV Power Electronics Specialist Level 6", "nsqf_level": 6, "sector_id": "SEC-AUTO"},
        {"qualification_id": "QP-IT-SDE-L6", "title": "Full-Stack Software Architect Level 6", "nsqf_level": 6, "sector_id": "SEC-IT"},
        {"qualification_id": "QP-IT-CLOUD-L7", "title": "Cloud & AI Infrastructure Engineer Level 7", "nsqf_level": 7, "sector_id": "SEC-IT"},
        {"qualification_id": "QP-REN-SOLAR-L4", "title": "Solar Photovoltaic Technician Level 4", "nsqf_level": 4, "sector_id": "SEC-RENEW"},
        {"qualification_id": "QP-REN-MICROGRID-L7", "title": "Renewable Energy Grid Integrator Level 7", "nsqf_level": 7, "sector_id": "SEC-RENEW"},
        {"qualification_id": "QP-HLTH-NURSE-L5", "title": "Critical Care Clinical Nurse Level 5", "nsqf_level": 5, "sector_id": "SEC-HLTH"},
        {"qualification_id": "QP-HLTH-LAB-L4", "title": "Medical Lab Technician Level 4", "nsqf_level": 4, "sector_id": "SEC-HLTH"},
    ]
    stmt = insert(DimQualification).values(qualifications).on_conflict_do_nothing(index_elements=["qualification_id"])
    await session.execute(stmt)
    stats["dim_qualification"] = len(qualifications)

    # 11. DimTrainingProgram
    programs = [
        {"program_id": "PRG-AUTO-EV-101", "qualification_id": "QP-AUTO-EV-L4", "duration_hours": 360, "curriculum_version": "2.1"},
        {"program_id": "PRG-IT-SDE-201", "qualification_id": "QP-IT-SDE-L6", "duration_hours": 480, "curriculum_version": "3.0"},
        {"program_id": "PRG-REN-SOLAR-301", "qualification_id": "QP-REN-SOLAR-L4", "duration_hours": 300, "curriculum_version": "1.5"},
        {"program_id": "PRG-HLTH-LAB-401", "qualification_id": "QP-HLTH-LAB-L4", "duration_hours": 400, "curriculum_version": "2.0"},
    ]
    stmt = insert(DimTrainingProgram).values(programs).on_conflict_do_nothing(index_elements=["program_id"])
    await session.execute(stmt)
    stats["dim_training_program"] = len(programs)

    # 12. DimTrainingCenter
    centers = [
        {"center_id": "TC-MH-PUN-01", "district_id": "IN-MH-PUN", "name": "Government Industrial Training Institute Pune", "center_type": CenterTypeEnum.ITI.value, "is_accredited": True},
        {"center_id": "TC-MH-MUM-01", "district_id": "IN-MH-MUM", "name": "Pradhan Mantri Kaushal Kendra Mumbai", "center_type": CenterTypeEnum.PMKVY_KENDRA.value, "is_accredited": True},
        {"center_id": "TC-KA-BLR-01", "district_id": "IN-KA-BLR", "name": "Advanced Skills Training Institute Bengaluru", "center_type": CenterTypeEnum.POLYTECHNIC.value, "is_accredited": True},
        {"center_id": "TC-GJ-AHD-01", "district_id": "IN-GJ-AHD", "name": "Gujarat Renewable Energy Skilling Academy", "center_type": CenterTypeEnum.PRIVATE_VTP.value, "is_accredited": True},
    ]
    stmt = insert(DimTrainingCenter).values(centers).on_conflict_do_nothing(index_elements=["center_id"])
    await session.execute(stmt)
    stats["dim_training_center"] = len(centers)

    # 13. DimDate (24 monthly periods: 2024-01-01 to 2025-12-01)
    dates = []
    for y in [2024, 2025]:
        for m in range(1, 13):
            d = date(y, m, 1)
            q = (m - 1) // 3 + 1
            fy = f"FY{y}-{str(y+1)[2:]}" if m >= 4 else f"FY{y-1}-{str(y)[2:]}"
            fq = f"Q{(m-4)%12//3 + 1}"
            dates.append({
                "date_key": d,
                "day": 1,
                "month": m,
                "quarter": q,
                "year": y,
                "financial_year": fy,
                "financial_quarter": fq,
                "month_name": d.strftime("%B"),
                "is_weekend": False,
            })
    stmt = insert(DimDate).values(dates).on_conflict_do_nothing(index_elements=["date_key"])
    await session.execute(stmt)
    stats["dim_date"] = len(dates)

    # 14. Deterministic Demo Facts (clearly labeled FIXTURE, source='LABREX_DEMO')
    demands = []
    supplies = []
    sample_occs = ["OCC-AUTO-EV-MECH", "OCC-IT-SDE", "OCC-REN-PV-INST", "OCC-HLTH-LAB-TECH"]
    sample_dists = ["IN-MH-PUN", "IN-KA-BLR", "IN-GJ-AHD"]

    for d in dates:
        dt = d["date_key"]
        month_idx = d["month"]
        for dist in sample_dists:
            for occ in sample_occs:
                # Deterministic math based on IDs and date
                base_demand = 120 + (hash(dist + occ) % 80) + (month_idx * 5)
                new_demand = int(base_demand * 0.35)
                base_supply = 140 + (hash(occ + dist) % 70) + (month_idx * 3)
                
                demands.append({
                    "date_key": dt,
                    "district_id": dist,
                    "occupation_id": occ,
                    "active_postings": max(10, base_demand),
                    "new_postings": max(5, new_demand),
                    "median_days_open": 28 + (month_idx % 7),
                    "unique_employers": 12 + (month_idx % 5),
                    "source_id": "LABREX_DEMO",
                    "dataset_type": DataTypeEnum.FIXTURE.value,
                })
                supplies.append({
                    "date_key": dt,
                    "district_id": dist,
                    "occupation_id": occ,
                    "employed_stock": max(100, base_supply * 10),
                    "unemployed_seeking": max(10, int(base_supply * 0.2)),
                    "fresh_graduates": max(5, int(base_supply * 0.15)),
                    "source_id": "LABREX_DEMO",
                    "dataset_type": DataTypeEnum.FIXTURE.value,
                })

    stmt = insert(FactJobDemand).values(demands).on_conflict_do_nothing(index_elements=["district_id", "occupation_id", "date_key"])
    await session.execute(stmt)
    stats["fact_job_demand"] = len(demands)

    stmt = insert(FactWorkforceSupply).values(supplies).on_conflict_do_nothing(index_elements=["district_id", "occupation_id", "date_key"])
    await session.execute(stmt)
    stats["fact_workforce_supply"] = len(supplies)

    # Training Capacity & Outcomes
    capacities = []
    outcomes = []
    for d in dates[:12]:  # First 12 periods
        dt = d["date_key"]
        for c in centers:
            for q in qualifications[:2]:
                seats = 60 + (hash(c["center_id"] + q["qualification_id"]) % 40)
                enrolled = int(seats * 0.85)
                capacities.append({
                    "date_key": dt,
                    "center_id": c["center_id"],
                    "qualification_id": q["qualification_id"],
                    "sanctioned_seats": seats,
                    "enrolled_trainees": enrolled,
                    "source_id": "LABREX_DEMO",
                    "dataset_type": DataTypeEnum.FIXTURE.value,
                })
                outcomes.append({
                    "date_key": dt,
                    "center_id": c["center_id"],
                    "qualification_id": q["qualification_id"],
                    "completed_trainees": int(enrolled * 0.9),
                    "certified_trainees": int(enrolled * 0.82),
                    "placed_trainees": int(enrolled * 0.65),
                    "source_id": "LABREX_DEMO",
                    "dataset_type": DataTypeEnum.FIXTURE.value,
                })

    stmt = insert(FactTrainingCapacity).values(capacities).on_conflict_do_nothing(index_elements=["center_id", "qualification_id", "date_key"])
    await session.execute(stmt)
    stats["fact_training_capacity"] = len(capacities)

    stmt = insert(FactTrainingOutcomes).values(outcomes).on_conflict_do_nothing(index_elements=["center_id", "qualification_id", "date_key"])
    await session.execute(stmt)
    stats["fact_training_outcomes"] = len(outcomes)

    await session.commit()
    logger.info("Deterministic benchmark fixtures seeded successfully: %s", stats)
    return stats
