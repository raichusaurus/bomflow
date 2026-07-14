import pytest


@pytest.mark.parametrize(
    ("bom", "message"),
    [
        ({}, "line_items"),
        ({"line_items": []}, "line_items"),
        ({"line_items": [{"quantity": 1}]}, "part_number"),
        ({"line_items": [{"part_number": "A", "quantity": 0}]}, "quantity"),
        ({"line_items": [{"part_number": "A", "quantity": -1}]}, "quantity"),
        ({"line_items": [{"part_number": "A", "quantity": True}]}, "quantity"),
    ],
)
def test_invalid_bom_is_rejected(generate_report, bom, message):
    with pytest.raises(ValueError, match=message):
        generate_report(bom, {"factors": []})


@pytest.mark.parametrize(
    ("catalog", "message"),
    [
        ({}, "factors"),
        ({"factors": [{}]}, "match_key"),
        ({"factors": [{"match_key": "A", "match_type": "other", "emission_factor_kgco2e": 1}]}, "match_type"),
        ({"factors": [{"match_key": "A", "match_type": "part_number", "emission_factor_kgco2e": -1}]}, "emission_factor_kgco2e"),
        ({"factors": [{"match_key": "A", "match_type": "part_number", "emission_factor_kgco2e": True}]}, "emission_factor_kgco2e"),
    ],
)
def test_invalid_catalog_is_rejected(generate_report, catalog, message):
    with pytest.raises(ValueError, match=message):
        generate_report({"line_items": [{"part_number": "A", "quantity": 1}]}, catalog)


def test_missing_confidence_becomes_visible_unknown_quality(generate_report):
    report = generate_report(
        {"line_items": [{"part_number": "A", "category": "x", "quantity": 1}]},
        {"factors": [{"match_key": "A", "match_type": "part_number", "emission_factor_kgco2e": 1}]},
    )
    assert report["line_items"][0]["confidence"] == "unknown"
    assert report["line_items"][0]["match_status"] == "low_confidence"
    assert report["data_quality_flags"][0]["flag_type"] == "low_confidence"
