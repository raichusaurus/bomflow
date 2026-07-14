def _bom(*lines):
    return {"bom_id": "matching", "line_items": list(lines)}


def _catalog(*factors):
    return {"catalog_id": "matching", "factors": list(factors)}


def _factor(key, kind, value, confidence="high"):
    return {
        "match_key": key,
        "match_type": kind,
        "emission_factor_kgco2e": value,
        "confidence": confidence,
    }


def test_part_match_wins_over_category_fallback(generate_report):
    report = generate_report(
        _bom({"part_number": "P-1", "category": " Widgets ", "quantity": 2}),
        _catalog(_factor(" P-1 ", "part_number", 3), _factor("widgets", "category", 9)),
    )
    line = report["line_items"][0]
    assert line["match_status"] == "matched"
    assert line["match_type"] == "part_number"
    assert line["subtotal_kgco2e"] == 6


def test_part_numbers_are_case_sensitive_but_categories_are_not(generate_report):
    report = generate_report(
        _bom({"part_number": "abc", "category": " Widgets ", "quantity": 1}),
        _catalog(_factor("ABC", "part_number", 4), _factor("widgets", " CATEGORY ", 2)),
    )
    assert report["line_items"][0]["match_status"] == "estimated"
    assert report["line_items"][0]["emission_factor_kgco2e"] == 2


def test_conflicting_factors_generate_partial_report(generate_report):
    report = generate_report(
        _bom({"part_number": "P-1", "category": "widget", "quantity": 1}),
        _catalog(_factor("P-1", "part_number", 2), _factor(" P-1 ", "part_number", 3)),
    )
    line = report["line_items"][0]
    flag = report["data_quality_flags"][0]
    assert line["match_status"] == "conflicting_factor"
    assert line["included_in_total"] is False
    assert line["emission_factor_kgco2e"] is None
    assert line["subtotal_kgco2e"] is None
    assert flag["flag_type"] == "conflicting_factor"
    assert flag["severity"] == "error"
    assert flag["details"]["catalog_rows"] == [1, 2]
    assert flag["details"]["factor_values"] == [2, 3]
    assert report["bom_summary"]["coverage_status"] == "partial"


def test_missing_category_is_independent_of_primary_match(generate_report):
    report = generate_report(
        _bom({"part_number": "P-1", "quantity": 1}),
        _catalog(_factor("P-1", "part_number", 1)),
    )
    line = report["line_items"][0]
    assert line["category"] == "uncategorized"
    assert line["match_status"] == "matched"
    assert {flag["flag_type"] for flag in report["data_quality_flags"]} == {"uncategorized"}
