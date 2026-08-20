from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any

SUPPORTED = {".md", ".markdown", ".txt", ".json", ".csv"}

CLAIM_PATTERNS = {
    "decision": re.compile(r"^\s*(?:decision|تصمیم)\s*[:：-]\s*(.+)$", re.I),
    "requirement": re.compile(r"^\s*(?:requirement|نیازمندی|الزام)\s*[:：-]\s*(.+)$", re.I),
    "risk": re.compile(r"^\s*(?:risk|ریسک)\s*[:：-]\s*(.+)$", re.I),
    "action": re.compile(r"^\s*(?:action|اقدام|todo)\s*[:：-]\s*(.+)$", re.I),
    "claim": re.compile(r"^\s*(?:claim|ادعا)\s*[:：-]\s*(.+)$", re.I),
}

NEGATION = re.compile(r"\b(?:not|no|never|cannot|نیست|نباید|نمی)\b", re.I)
SUBJECT = re.compile(r"(?:decision|requirement|risk|action|claim|تصمیم|نیازمندی|الزام|ریسک|اقدام|ادعا)\s*[:：-]\s*", re.I)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _read(path: Path) -> str:
    if path.suffix.lower() == ".json":
        obj = json.loads(path.read_text(encoding="utf-8"))
        return json.dumps(obj, ensure_ascii=False, indent=2)
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8", newline="") as fh:
            return "\n".join(", ".join(row) for row in csv.reader(fh))
    return path.read_text(encoding="utf-8", errors="replace")


def _documents(source: Path) -> list[Path]:
    if source.is_file():
        return [source] if source.suffix.lower() in SUPPORTED else []
    return sorted(p for p in source.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED)


def ingest_path(source: str | Path, output: str | Path) -> dict[str, Any]:
    source, output = Path(source), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    docs: list[dict[str, Any]] = []
    for path in _documents(source):
        text = _read(path)
        rel = str(path.relative_to(source)) if source.is_dir() else path.name
        docs.append({
            "document_id": "DOC-" + sha256_text(rel + "\n" + text)[:12],
            "path": rel,
            "filename": path.name,
            "format": path.suffix.lower().lstrip("."),
            "sha256": sha256_text(text),
            "bytes": len(text.encode("utf-8")),
            "lines": len(text.splitlines()),
            "status": "INGESTED",
        })
    registry = {"schema_version": "0.1", "documents": docs}
    (output / "document_registry.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    return registry


def _subject(text: str) -> str:
    text = SUBJECT.sub("", text).strip().lower()
    text = re.sub(r"[^\w\s-]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def _extract_claims(doc: dict[str, Any], source_root: Path) -> list[dict[str, Any]]:
    path = source_root / doc["path"]
    lines = _read(path).splitlines()
    claims = []
    for number, line in enumerate(lines, 1):
        for kind, pattern in CLAIM_PATTERNS.items():
            match = pattern.match(line)
            if not match:
                continue
            text = match.group(1).strip()
            claims.append({
                "claim_id": "CLM-" + sha256_text(doc["document_id"] + f":{number}:{text}")[:12],
                "document_id": doc["document_id"],
                "type": kind,
                "text": text,
                "subject": _subject(line),
                "evidence": {
                    "document_id": doc["document_id"],
                    "path": doc["path"],
                    "line_start": number,
                    "line_end": number,
                    "quote": line.strip(),
                },
                "polarity": "negative" if NEGATION.search(text) else "positive",
                "validation_status": "CANDIDATE",
            })
            break
    return claims


def analyze_workspace(workspace: str | Path, source_root: str | Path | None = None) -> dict[str, Any]:
    workspace = Path(workspace)
    registry = json.loads((workspace / "document_registry.json").read_text(encoding="utf-8"))
    source_root = Path(source_root or workspace.parent)
    all_claims: list[dict[str, Any]] = []
    for doc in registry["documents"]:
        all_claims.extend(_extract_claims(doc, source_root))

    groups: dict[str, list[dict[str, Any]]] = {}
    for claim in all_claims:
        if claim["subject"]:
            groups.setdefault(claim["subject"], []).append(claim)

    conflicts = []
    for subject, claims in groups.items():
        polarities = {c["polarity"] for c in claims}
        if len(claims) > 1 and len(polarities) > 1:
            conflicts.append({
                "conflict_id": "CNF-" + sha256_text(subject)[:12],
                "subject": subject,
                "claim_ids": [c["claim_id"] for c in claims],
                "status": "UNRESOLVED",
                "reason": "Opposite polarity candidates share the same normalized subject.",
            })

    dependencies = []
    for claim in all_claims:
        dependencies.append({
            "from": claim["document_id"],
            "to": claim["claim_id"],
            "type": "SUPPORTS",
        })

    gaps = []
    for claim in all_claims:
        if claim["validation_status"] != "VALIDATED":
            gaps.append({
                "gap_id": "GAP-" + sha256_text(claim["claim_id"])[:12],
                "claim_id": claim["claim_id"],
                "type": "HUMAN_VALIDATION_REQUIRED",
                "severity": "MEDIUM",
            })
    result = {
        "schema_version": "0.1",
        "product": "PKEA",
        "documents": registry["documents"],
        "claims": all_claims,
        "conflicts": conflicts,
        "dependencies": dependencies,
        "gaps": gaps,
        "controls": {
            "unsupported_claims_promoted": False,
            "human_gate_required": True,
            "canonicalization": "PROHIBITED_IN_MVP",
        },
    }
    (workspace / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def write_report(workspace: str | Path, output: str | Path | None = None) -> Path:
    workspace = Path(workspace)
    output = Path(output or workspace / "report.md")
    data = json.loads((workspace / "analysis.json").read_text(encoding="utf-8"))
    lines = [
        "# Project Knowledge & Evidence Agent — Audit Package",
        "",
        f"Documents: **{len(data['documents'])}**  ",
        f"Candidate claims: **{len(data['claims'])}**  ",
        f"Unresolved conflicts: **{len(data['conflicts'])}**  ",
        f"Evidence gaps: **{len(data['gaps'])}**",
        "",
        "## Claims and evidence",
    ]
    for claim in data["claims"]:
        e = claim["evidence"]
        lines += [
            f"### {claim['claim_id']} — {claim['type']}",
            claim["text"],
            f"- Source: `{e['path']}` lines {e['line_start']}-{e['line_end']}",
            f"- Status: `{claim['validation_status']}`",
            "",
        ]
    lines += ["## Conflicts"]
    if data["conflicts"]:
        for c in data["conflicts"]:
            lines.append(f"- `{c['conflict_id']}` — {c['subject']} — {c['status']}")
    else:
        lines.append("- None detected by the MVP rules.")
    lines += ["", "## Governance"]
    lines += [
        "- No candidate is canonical by default.",
        "- Source locations are retained for traceability.",
        "- Conflicts remain unresolved until human review.",
    ]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
