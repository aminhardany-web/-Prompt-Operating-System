from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pkea.core import analyze_workspace, ingest_path  # noqa: E402


def main() -> int:
    base = Path(__file__).resolve().parent
    source = base / "golden_project"
    workspace = base / ".workspace"
    expected = json.loads((source / "golden.json").read_text(encoding="utf-8"))
    registry = ingest_path(source, workspace)
    result = analyze_workspace(workspace, source)

    type_counts: dict[str, int] = {}
    for claim in result["claims"]:
        type_counts[claim["type"]] = type_counts.get(claim["type"], 0) + 1

    checks = {
        "documents": len(registry["documents"]) == expected["expected_documents"],
        "claims": len(result["claims"]) == expected["expected_claims"],
        "conflicts": len(result["conflicts"]) == expected["expected_conflicts"],
        "claim_types": type_counts == expected["expected_claim_types"],
        "traceability": all(c["evidence"]["path"] and c["evidence"]["line_start"] for c in result["claims"]),
        "human_gate": result["controls"]["human_gate_required"] is True,
    }
    passed = sum(checks.values())
    report = {
        "checks": checks,
        "passed": passed,
        "total": len(checks),
        "score": round(passed / len(checks), 4),
    }
    (base / "evaluation_result.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
