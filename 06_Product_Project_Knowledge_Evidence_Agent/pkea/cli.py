from __future__ import annotations

import argparse
from pathlib import Path

from .core import analyze_workspace, ingest_path, write_report


def main() -> None:
    parser = argparse.ArgumentParser(prog="pkea", description="Project Knowledge & Evidence Agent")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="register project source documents")
    ingest.add_argument("source")
    ingest.add_argument("--output", default="./workspace")

    analyze = sub.add_parser("analyze", help="extract claims and evidence")
    analyze.add_argument("workspace")
    analyze.add_argument("--source-root", default=None)

    report = sub.add_parser("report", help="write an audit-ready Markdown report")
    report.add_argument("workspace")
    report.add_argument("--output", default=None)

    args = parser.parse_args()
    if args.command == "ingest":
        result = ingest_path(args.source, args.output)
        print(f"Registered {len(result['documents'])} documents in {args.output}")
    elif args.command == "analyze":
        result = analyze_workspace(args.workspace, args.source_root)
        print(f"Claims={len(result['claims'])} Conflicts={len(result['conflicts'])} Gaps={len(result['gaps'])}")
    else:
        path = write_report(args.workspace, args.output)
        print(Path(path).resolve())


if __name__ == "__main__":
    main()
