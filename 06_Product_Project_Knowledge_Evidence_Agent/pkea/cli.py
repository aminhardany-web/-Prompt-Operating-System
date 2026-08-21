from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import analyze_workspace, ingest_path, write_report
from .review import append_review


def _run(source: str, output: str, llm: str) -> dict:
    workspace = Path(output).resolve()
    registry = ingest_path(source, workspace)
    adapter = None
    if llm == "openai":
        from .llm_adapter import OpenAIResponsesAdapter
        adapter = OpenAIResponsesAdapter.from_env()
    result = analyze_workspace(workspace, adapter=adapter)
    report = write_report(workspace)
    summary = {
        "product": "PKEA",
        "source": str(Path(source).resolve()),
        "workspace": str(workspace),
        "documents": len(registry["documents"]),
        "claims": len(result["claims"]),
        "conflicts": len(result["conflicts"]),
        "gaps": len(result["gaps"]),
        "extraction_mode": result["controls"]["extraction_mode"],
        "llm_claims_rejected_by_evidence_validation": result["controls"]["llm_claims_rejected_by_evidence_validation"],
        "artifacts": [
            "document_registry.json",
            "analysis.json",
            "report.md",
            "run_summary.json",
        ],
        "status": "COMPLETED",
    }
    (workspace / "run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(prog="pkea", description="Project Knowledge & Evidence Agent")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="execute the complete deterministic PKEA pipeline")
    run.add_argument("source")
    run.add_argument("--output", default="./workspace")
    run.add_argument("--llm", choices=["none", "openai"], default="none")

    ingest = sub.add_parser("ingest", help="register project source documents")
    ingest.add_argument("source")
    ingest.add_argument("--output", default="./workspace")

    analyze = sub.add_parser("analyze", help="extract claims and evidence")
    analyze.add_argument("workspace")
    analyze.add_argument("--source-root", default=None)
    analyze.add_argument("--llm", choices=["none", "openai"], default="none")

    review = sub.add_parser("review", help="append a human validation decision to the audit ledger")
    review.add_argument("workspace")
    review.add_argument("claim_id")
    review.add_argument("--decision", choices=["VALIDATED", "REJECTED", "NEEDS_REVIEW"], required=True)
    review.add_argument("--reviewer", required=True)
    review.add_argument("--note", default="")

    report = sub.add_parser("report", help="write an audit-ready Markdown report")
    report.add_argument("workspace")
    report.add_argument("--output", default=None)

    args = parser.parse_args()
    if args.command == "run":
        result = _run(args.source, args.output, args.llm)
        print(
            f"PKEA completed: Documents={result['documents']} Claims={result['claims']} "
            f"Conflicts={result['conflicts']} Gaps={result['gaps']} Mode={result['extraction_mode']}"
        )
    elif args.command == "ingest":
        result = ingest_path(args.source, args.output)
        print(f"Registered {len(result['documents'])} documents in {args.output}")
    elif args.command == "analyze":
        adapter = None
        if args.llm == "openai":
            from .llm_adapter import OpenAIResponsesAdapter
            adapter = OpenAIResponsesAdapter.from_env()
        result = analyze_workspace(args.workspace, args.source_root, adapter=adapter)
        print(
            f"Claims={len(result['claims'])} Conflicts={len(result['conflicts'])} "
            f"Gaps={len(result['gaps'])} Mode={result['controls']['extraction_mode']}"
        )
    elif args.command == "review":
        event = append_review(
            args.workspace,
            claim_id=args.claim_id,
            decision=args.decision,
            reviewer=args.reviewer,
            note=args.note,
        )
        print(f"Recorded {event['event_id']} for {event['claim_id']}: {event['decision']}")
    else:
        path = write_report(args.workspace, args.output)
        print(Path(path).resolve())


if __name__ == "__main__":
    main()
