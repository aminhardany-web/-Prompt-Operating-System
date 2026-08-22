from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
RESOURCE_ROOT = ROOT / "resources" / "library"

import sys
sys.path.insert(0, str(ROOT))

from pkea.core import analyze_workspace, ingest_path  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "workspace"
        registry = ingest_path(RESOURCE_ROOT, workspace)
        result = analyze_workspace(workspace)

    checks = {
        "resource_documents_ingested": len(registry["documents"]) >= 4,
        "claims_have_evidence": all(c["evidence"]["path"] and c["evidence"]["line_start"] for c in result["claims"]),
        "human_gate": result["controls"]["human_gate_required"] is True,
        "snapshot_analysis": result["controls"]["analysis_source"] == "INGESTED_SNAPSHOT",
        "no_auto_canonicalization": result["controls"]["canonicalization"] == "PROHIBITED_IN_MVP",
    }
    report = {
        "resource_root": str(RESOURCE_ROOT.relative_to(REPO_ROOT)),
        "documents": len(registry["documents"]),
        "claims": len(result["claims"]),
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
