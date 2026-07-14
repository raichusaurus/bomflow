import json
import subprocess
import sys


def _command(root, out, *extra):
    return [
        sys.executable,
        "-m",
        "bomflow",
        "report",
        "--bom",
        str(root / "data/fixtures/canonical-iot-sensor.bom.json"),
        "--catalog",
        str(root / "data/catalogs/mock-emissions-catalog.json"),
        "--out",
        str(out),
        *extra,
    ]


def test_cli_writes_partial_report_and_exits_zero_by_default(tmp_path):
    root = __import__("pathlib").Path(__file__).resolve().parents[1]
    out = tmp_path / "nested" / "report.json"
    result = subprocess.run(_command(root, out), cwd=root, text=True, capture_output=True)

    assert result.returncode == 0, result.stderr
    assert out.exists()
    report = json.loads(out.read_text())
    assert report["bom_summary"]["total_estimated_kgco2e"] == 17.3
    assert "2 excluded lines" in result.stdout
    assert str(out) in result.stdout


def test_cli_strict_mode_writes_report_then_exits_nonzero(tmp_path):
    root = __import__("pathlib").Path(__file__).resolve().parents[1]
    out = tmp_path / "report.json"
    result = subprocess.run(_command(root, out, "--fail-on-data-errors"), cwd=root, text=True, capture_output=True)

    assert result.returncode != 0
    assert out.exists()
    assert json.loads(out.read_text())["bom_summary"]["coverage_status"] == "partial"


def test_cli_invalid_json_is_fatal_and_writes_no_report(tmp_path):
    root = __import__("pathlib").Path(__file__).resolve().parents[1]
    bad_bom = tmp_path / "bad.json"
    bad_bom.write_text("not json")
    out = tmp_path / "report.json"
    command = _command(root, out)
    command[command.index("--bom") + 1] = str(bad_bom)

    result = subprocess.run(command, cwd=root, text=True, capture_output=True)

    assert result.returncode != 0
    assert not out.exists()
    assert "json" in result.stderr.lower()
