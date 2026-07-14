from datetime import datetime

import pytest


REQUIRED_TOP_LEVEL_KEYS = {
    "report_metadata",
    "bom_summary",
    "top_carbon_contributors",
    "line_items",
    "data_quality_flags",
    "review_notes",
    "methodology_caveat",
}

REQUIRED_LINE_KEYS = {
    "part_number",
    "description",
    "category",
    "quantity",
    "match_status",
    "match_type",
    "emission_factor_kgco2e",
    "subtotal_kgco2e",
    "confidence",
    "source_note",
    "included_in_total",
}


def test_canonical_report_contract(generate_report, canonical_bom, canonical_catalog):
    report = generate_report(canonical_bom, canonical_catalog)

    assert set(report) == REQUIRED_TOP_LEVEL_KEYS
    assert report["bom_summary"] == {
        "part_count": 10,
        "quantity_count": 39,
        "total_estimated_kgco2e": pytest.approx(17.3),
        "data_quality_flag_count": 6,
        "excluded_line_count": 2,
        "coverage_status": "partial",
    }
    assert len(report["line_items"]) == 10
    assert all(set(line) == REQUIRED_LINE_KEYS for line in report["line_items"])

    flag_types = [flag["flag_type"] for flag in report["data_quality_flags"]]
    assert flag_types.count("estimated_factor") == 2
    assert flag_types.count("low_confidence") == 1
    assert flag_types.count("conflicting_factor") == 1
    assert flag_types.count("missing_factor") == 1
    assert flag_types.count("uncategorized") == 1
    assert all({"flag_type", "severity", "part_number", "message"} <= set(flag) for flag in report["data_quality_flags"])


def test_report_retains_all_ranked_contributors(generate_report, canonical_bom, canonical_catalog):
    report = generate_report(canonical_bom, canonical_catalog)
    contributors = report["top_carbon_contributors"]

    assert [item["part_number"] for item in contributors["line_items"]] == [
        "BAT-001", "PCB-001", "MCU-001", "SNS-001",
        "CON-001", "RES-PACK", "CAP-PACK", "LBL-001",
    ]
    assert [item["category"] for item in contributors["categories"]] == [
        "power", "pcb", "processor", "sensor", "connector", "passives", "uncategorized",
    ]


def test_timestamp_and_caveat_contract(generate_report, canonical_bom, canonical_catalog):
    report = generate_report(canonical_bom, canonical_catalog)

    generated_at = datetime.fromisoformat(report["report_metadata"]["generated_at"].replace("Z", "+00:00"))
    assert generated_at.tzinfo is not None
    assert "mock" in report["methodology_caveat"].lower()
    assert "compliance" in report["methodology_caveat"].lower()
    assert report["review_notes"]
