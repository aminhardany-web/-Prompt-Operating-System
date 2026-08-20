import json
from pathlib import Path

from pkea.core import analyze_workspace, ingest_path, write_report


def test_ingest_analyze_report(tmp_path: Path):
    source = tmp_path / "project"
    source.mkdir()
    (source / "a.md").write_text("# Project\nDecision: Use controlled change.\nRisk: stale source.\n", encoding="utf-8")
    (source / "b.md").write_text("Decision: Do not use controlled change.\n", encoding="utf-8")
    workspace = tmp_path / "workspace"

    registry = ingest_path(source, workspace)
    assert len(registry["documents"]) == 2

    result = analyze_workspace(workspace, source)
    assert len(result["claims"]) == 3
    assert len(result["conflicts"]) == 1
    assert all(c["validation_status"] == "CANDIDATE" for c in result["claims"])

    report = write_report(workspace)
    assert report.exists()
    parsed = json.loads((workspace / "analysis.json").read_text(encoding="utf-8"))
    assert parsed["controls"]["human_gate_required"] is True
