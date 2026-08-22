from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def append_review(
    workspace: str | Path,
    *,
    claim_id: str,
    decision: str,
    reviewer: str,
    note: str = "",
) -> dict[str, Any]:
    if decision not in {"VALIDATED", "REJECTED", "NEEDS_REVIEW"}:
        raise ValueError("decision must be VALIDATED, REJECTED, or NEEDS_REVIEW")
    workspace = Path(workspace)
    analysis = json.loads((workspace / "analysis.json").read_text(encoding="utf-8"))
    claim_ids = {claim["claim_id"] for claim in analysis["claims"]}
    if claim_id not in claim_ids:
        raise ValueError(f"Unknown claim_id: {claim_id}")

    event = {
        "event_id": f"REV-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "claim_id": claim_id,
        "decision": decision,
        "reviewer": reviewer,
        "note": note,
    }
    ledger = workspace / "validation_ledger.jsonl"
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def latest_reviews(workspace: str | Path) -> dict[str, dict[str, Any]]:
    ledger = Path(workspace) / "validation_ledger.jsonl"
    if not ledger.exists():
        return {}
    latest: dict[str, dict[str, Any]] = {}
    for line in ledger.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        latest[event["claim_id"]] = event
    return latest
