import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def generate_report():
    from bomflow import generate_report as public_generate_report

    return public_generate_report


@pytest.fixture
def canonical_bom():
    return json.loads((ROOT / "data/fixtures/canonical-iot-sensor.bom.json").read_text())


@pytest.fixture
def canonical_catalog():
    return json.loads((ROOT / "data/catalogs/mock-emissions-catalog.json").read_text())
