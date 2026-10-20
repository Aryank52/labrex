"""
LABREX Administrative Geography Parser & Validator
Authority: Master Directive Section 14 & Secondary Mandate Step 10
Source: Survey of India (SOI) & Local Government Directory (LGD)
"""

import json
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from pydantic import BaseModel, Field
from shapely.geometry import MultiPolygon, Polygon, shape


class GeographyValidationResult(BaseModel):
    is_valid: bool
    feature_id: str
    feature_type: str  # 'STATE' or 'DISTRICT'
    name: str
    code: str
    parent_state_code: Optional[str] = None
    geometry_valid: bool
    srid_valid: bool
    bounding_box_valid: bool
    centroid_lon: float
    centroid_lat: float
    violations: List[str] = Field(default_factory=list)


# Bounding box of India territorial mainland and islands (approximate envelope)
INDIA_BBOX = {
    "min_lon": 68.0,
    "max_lon": 98.0,
    "min_lat": 6.0,
    "max_lat": 38.0
}


class GeographyParser:
    """
    Parser and topological validator for official Indian administrative boundaries.
    Validates geometry validity (Shapely is_valid), SRID (EPSG:4326),
    geographical bounds, and parent-child state-district relationships.
    """

    def __init__(self, srid: int = 4326):
        self.srid = srid

    def validate_geometry(self, geom_dict: Dict[str, Any]) -> Tuple[bool, Optional[Any], List[str]]:
        """Validates that geojson geometry is valid, non-empty Polygon/MultiPolygon."""
        violations = []
        try:
            geom = shape(geom_dict)
            if not geom.is_valid:
                violations.append("Geometry is topologically invalid (self-intersection or duplicate vertices)")
            if geom.is_empty:
                violations.append("Geometry is empty")
            if not isinstance(geom, (Polygon, MultiPolygon)):
                violations.append(f"Expected Polygon or MultiPolygon, got {geom.geom_type}")
            return len(violations) == 0, geom, violations
        except Exception as e:
            return False, None, [f"Failed to parse geometry: {str(e)}"]

    def validate_bounds(self, geom: Any) -> Tuple[bool, List[str]]:
        """Verifies coordinates lie within the India territorial bounding envelope."""
        violations = []
        min_lon, min_lat, max_lon, max_lat = geom.bounds
        if min_lon < INDIA_BBOX["min_lon"] or max_lon > INDIA_BBOX["max_lon"]:
            violations.append(f"Longitude span [{min_lon:.2f}, {max_lon:.2f}] outside India bounds [{INDIA_BBOX['min_lon']}, {INDIA_BBOX['max_lon']}]")
        if min_lat < INDIA_BBOX["min_lat"] or max_lat > INDIA_BBOX["max_lat"]:
            violations.append(f"Latitude span [{min_lat:.2f}, {max_lat:.2f}] outside India bounds [{INDIA_BBOX['min_lat']}, {INDIA_BBOX['max_lat']}]")
        return len(violations) == 0, violations

    def parse_state_feature(self, feature: Dict[str, Any]) -> GeographyValidationResult:
        """Parses and validates an individual State GeoJSON feature."""
        props = feature.get("properties", {})
        code = str(props.get("state_code") or props.get("state_id") or props.get("code") or "IN-UNKNOWN").upper()
        name = str(props.get("state_name") or props.get("name") or code)

        geom_dict = feature.get("geometry", {})
        geom_valid, geom, geom_violations = self.validate_geometry(geom_dict)

        bbox_valid = False
        bbox_violations: List[str] = []
        centroid_lon, centroid_lat = 0.0, 0.0

        if geom_valid and geom:
            bbox_valid, bbox_violations = self.validate_bounds(geom)
            centroid_lon = round(geom.centroid.x, 6)
            centroid_lat = round(geom.centroid.y, 6)

        violations = geom_violations + bbox_violations
        return GeographyValidationResult(
            is_valid=len(violations) == 0,
            feature_id=f"STATE-{code}",
            feature_type="STATE",
            name=name,
            code=code,
            geometry_valid=geom_valid,
            srid_valid=(self.srid == 4326),
            bounding_box_valid=bbox_valid,
            centroid_lon=centroid_lon,
            centroid_lat=centroid_lat,
            violations=violations
        )

    def parse_district_feature(
        self,
        feature: Dict[str, Any],
        known_state_codes: Optional[Set[str]] = None
    ) -> GeographyValidationResult:
        """Parses and validates an individual District GeoJSON feature."""
        props = feature.get("properties", {})
        code = str(props.get("district_code") or props.get("district_id") or props.get("code") or "IN-DT-UNKNOWN").upper()
        name = str(props.get("district_name") or props.get("name") or code)
        parent_state = str(props.get("state_code") or props.get("state_id") or "").upper()

        geom_dict = feature.get("geometry", {})
        geom_valid, geom, geom_violations = self.validate_geometry(geom_dict)

        bbox_valid = False
        bbox_violations: List[str] = []
        centroid_lon, centroid_lat = 0.0, 0.0

        if geom_valid and geom:
            bbox_valid, bbox_violations = self.validate_bounds(geom)
            centroid_lon = round(geom.centroid.x, 6)
            centroid_lat = round(geom.centroid.y, 6)

        relational_violations = []
        if not parent_state:
            relational_violations.append("Missing parent state_code in district feature")
        elif known_state_codes and parent_state not in known_state_codes:
            relational_violations.append(f"Orphan district: parent state '{parent_state}' not found in known states")

        violations = geom_violations + bbox_violations + relational_violations
        return GeographyValidationResult(
            is_valid=len(violations) == 0,
            feature_id=f"DISTRICT-{code}",
            feature_type="DISTRICT",
            name=name,
            code=code,
            parent_state_code=parent_state if parent_state else None,
            geometry_valid=geom_valid,
            srid_valid=(self.srid == 4326),
            bounding_box_valid=bbox_valid,
            centroid_lon=centroid_lon,
            centroid_lat=centroid_lat,
            violations=violations
        )

    def parse_geojson_collection(
        self,
        geojson_data: Union[str, bytes, Dict[str, Any]],
        expected_type: str = "DISTRICT",
        known_state_codes: Optional[Set[str]] = None
    ) -> List[GeographyValidationResult]:
        """Parses a full FeatureCollection."""
        if isinstance(geojson_data, (str, bytes)):
            data = json.loads(geojson_data)
        else:
            data = geojson_data

        features = data.get("features", [])
        results = []
        for feat in features:
            if expected_type.upper() == "STATE":
                results.append(self.parse_state_feature(feat))
            else:
                results.append(self.parse_district_feature(feat, known_state_codes))
        return results
