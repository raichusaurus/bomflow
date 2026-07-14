import pytest


def test_rounds_lines_before_aggregating_visible_values(generate_report):
    report = generate_report(
        {
            "line_items": [
                {"part_number": "B", "category": "same", "quantity": 1},
                {"part_number": "A", "category": "same", "quantity": 1},
            ]
        },
        {
            "factors": [
                {"match_key": "A", "match_type": "part_number", "emission_factor_kgco2e": 1.2346, "confidence": "high"},
                {"match_key": "B", "match_type": "part_number", "emission_factor_kgco2e": 1.2346, "confidence": "high"},
            ]
        },
    )
    assert [line["subtotal_kgco2e"] for line in report["line_items"]] == [1.235, 1.235]
    assert report["bom_summary"]["total_estimated_kgco2e"] == pytest.approx(2.47)
    assert report["top_carbon_contributors"]["categories"][0]["subtotal_kgco2e"] == pytest.approx(2.47)
    assert [line["part_number"] for line in report["top_carbon_contributors"]["line_items"]] == ["A", "B"]


def test_empty_catalog_generates_all_missing_zero_total(generate_report):
    report = generate_report(
        {"line_items": [{"part_number": "A", "category": "x", "quantity": 2}]},
        {"factors": []},
    )
    assert report["bom_summary"]["total_estimated_kgco2e"] == 0
    assert report["bom_summary"]["excluded_line_count"] == 1
    assert report["bom_summary"]["coverage_status"] == "partial"
    assert report["top_carbon_contributors"] == {"line_items": [], "categories": []}


def test_zero_factor_warning_is_opt_in(generate_report):
    bom = {"line_items": [{"part_number": "ZERO", "category": "x", "quantity": 1}]}
    catalog = {"factors": [{"match_key": "ZERO", "match_type": "part_number", "emission_factor_kgco2e": 0, "confidence": "high"}]}

    default_report = generate_report(bom, catalog)
    warned_report = generate_report(bom, catalog, warn_on_zero_factor=True)

    assert default_report["data_quality_flags"] == []
    assert warned_report["data_quality_flags"][0]["flag_type"] == "zero_factor"
    assert warned_report["line_items"][0]["included_in_total"] is True
    assert warned_report["bom_summary"]["coverage_status"] == "complete"
