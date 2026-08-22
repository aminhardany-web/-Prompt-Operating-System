from __future__ import annotations

import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from .review import latest_reviews

SUPPORTED = {".md", ".markdown", ".txt", ".json", ".csv", ".docx"}

CLAIM_PATTERNS = {
    "decision": re.compile(r"^\s*(?:decision|تصمیم)\s*[:：-]\s*(.+)$", re.I),
    "requirement": re.compile(r"^\s*(?:requirement|نیازمندی|الزام)\s*[:：-]\s*(.+)$", re.I),
    "risk": re.compile(r"^\s*(?:risk|ریسک)\s*[:：-]\s*(.+)$", re.I),
    "action": re.compile(r"^\s*(?:action|اقدام|todo)\s*[:：-]\s*(.+)$", re.I),
    "claim": re.compile(r"^\s*(?:claim|ادعا)\s*[:：-]\s*(.+)$", re.I),
}
NEGATION = re.compile(r"\b(?:not|no|never|cannot|do not|does not|did not|نیست|نباید|نمی|نه)\b", re.I)
SUBJECT_PREFIX = re.compile(r"(?:decision|requirement|risk|action|claim|تصمیم|نیازمندی|الزام|ریسک|اقدام|ادعا)\s*[:：-]\s*", re.I)
NEGATION_PHRASES = re.compile(r"\b(?:do not|does not|did not|cannot|never|not|no)\b", re.I)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _read_docx(path: Path) -> str:
    """Extract visible DOCX body paragraphs while preserving evidence line positions.

    Paragraph boundaries are preserved, including empty paragraphs, because the
    extracted snapshot is the audit source for deterministic line evidence.
    Word tabs and explicit line breaks are retained rather than discarded.
    """
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml")
    except (KeyError, zipfile.BadZipFile) as exc:
        raise ValueError(f"Invalid DOCX package: {path}") from exc

    try:
        root = ET.fromstring(xml)
    except ET.ParseError as exc:
        raise ValueError(f"Invalid DOCX XML: {path}") from exc

    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:body/w:p", namespace):
        chunks: list[str] = []
        for node in paragraph.iter():
            if node.tag == f"{{{namespace['w']}}}t":
                chunks.append(node.text or "")
            elif node.tag == f"{{{namespace['w']}}}tab":
                chunks.append("\t")
            elif node.tag in {
                f"{{{namespace['w']}}}br",
                f"{{{namespace['w']}}}cr",
            }:
                chunks.append("\n")
        paragraphs.append("".join(chunks).strip())
    return "\n".join(paragraphs)


def _read(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return _read_docx(path)
    if suffix == ".json":
        obj = json.loads(path.read_text(encoding="utf-8"))
        return json.dumps(obj, ensure_ascii=False, indent=2)
    if suffix == ".csv":
        with path.open("r", encoding="utf-8", newline="") as fh:
            return "\n".join(", ".join(row) for row in csv.reader(fh))
    return path.read_text(encoding="utf-8", errors="replace")


def _documents(source: Path, output: Path | None = None) -> list[Path]:
    if source.is_file():
        return [source] if source.suffix.lower() in SUPPORTED else []
    output = output.resolve() if output else None
    paths: list[Path] = []
    for path in source.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue
        if output and (path == output or output in path.parents):
            continue
        paths.append(path)
    return sorted(paths)


def ingest_path(source: str | Path, output: str | Path) -> dict[str, Any]:
    source, output = Path(source).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    snapshots = output / "source_snapshots"
    snapshots.mkdir(parents=True, exist_ok=True)
    docs: list[dict[str, Any]] = []
    for path in _documents(source, output):
        text = _read(path)
        rel = str(path.relative_to(source)) if source.is_dir() else path.name
        document_id = "DOC-" + sha256_text(rel + "\n" + text)[:12]
        snapshot_name = f"{document_id}.txt"
        (snapshots / snapshot_name).write_text(text, encoding="utf-8")
        docs.append({"document_id": document_id, "path": rel, "filename": path.name, "format": path.suffix.lower().lstrip("."), "sha256": sha256_text(text), "bytes": len(text.encode("utf-8")), "lines": len(text.splitlines()), "snapshot_path": f"source_snapshots/{snapshot_name}", "status": "INGESTED"})
    registry = {"schema_version": "0.3", "source_root": str(source), "snapshot_policy": "ANALYZE_FROM_INGESTED_SNAPSHOT", "documents": docs}
    (output / "document_registry.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    return registry


def _subject(text: str) -> str:
    value = SUBJECT_PREFIX.sub("", text).strip().lower()
    value = NEGATION_PHRASES.sub(" ", value)
    value = re.sub(r"\b(?:is|are|was|were|be|should|must|can|cannot|use|uses|used|است|هست|باشد|باید|نباید)\b", " ", value, flags=re.I)
    value = re.sub(r"[^\w\s-]", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def _candidate(doc: dict[str, Any], text: str, line_start: int, line_end: int, quote: str, kind: str) -> dict[str, Any]:
    return {"claim_id": "CLM-" + sha256_text(doc["document_id"] + f":{line_start}:{line_end}:{text}")[:12], "document_id": doc["document_id"], "type": kind, "text": text.strip(), "subject": _subject(f"{kind}: {text}"), "evidence": {"document_id": doc["document_id"], "path": doc["path"], "line_start": line_start, "line_end": line_end, "quote": quote.strip()}, "polarity": "negative" if NEGATION.search(text) else "positive", "validation_status": "CANDIDATE"}


def _snapshot_lines(workspace: Path, doc: dict[str, Any]) -> list[str]:
    return (workspace / doc["snapshot_path"]).read_text(encoding="utf-8").splitlines()


def _extract_claims(doc: dict[str, Any], workspace: Path) -> list[dict[str, Any]]:
    lines = _snapshot_lines(workspace, doc)
    claims: list[dict[str, Any]] = []
    for number, line in enumerate(lines, 1):
        for kind, pattern in CLAIM_PATTERNS.items():
            match = pattern.match(line)
            if match:
                claims.append(_candidate(doc, match.group(1).strip(), number, number, line, kind))
                break
    return claims


def _normalize_tokens(value: str) -> set[str]:
    return {token for token in re.split(r"\s+", re.sub(r"[^\w\s-]", " ", value.lower(), flags=re.UNICODE)) if len(token) > 2}


def _claim_text_is_grounded(text: str, source_quote: str) -> bool:
    claim_tokens = _normalize_tokens(text)
    source_tokens = _normalize_tokens(source_quote)
    if not claim_tokens:
        return False
    polarity_conflict = NEGATION.search(text) is not None and NEGATION.search(source_quote) is None
    return claim_tokens.issubset(source_tokens) and not polarity_conflict


def _validate_llm_claim(doc: dict[str, Any], lines: list[str], raw: dict[str, Any]) -> dict[str, Any] | None:
    kind = str(raw.get("type", "claim")).lower()
    if kind not in CLAIM_PATTERNS:
        kind = "claim"
    try:
        start, end = int(raw["line_start"]), int(raw.get("line_end", raw["line_start"]))
    except (KeyError, TypeError, ValueError):
        return None
    if start < 1 or end < start or end > len(lines):
        return None
    source_quote = "\n".join(lines[start - 1:end]).strip()
    quote = str(raw.get("quote", "")).strip()
    text = str(raw.get("text", "")).strip()
    if quote and quote != source_quote:
        return None
    if not text or not _claim_text_is_grounded(text, source_quote):
        return None
    return _candidate(doc, text, start, end, source_quote, kind)


def _extract_llm_claims(doc: dict[str, Any], workspace: Path, adapter: Any) -> tuple[list[dict[str, Any]], int]:
    lines = _snapshot_lines(workspace, doc)
    numbered = "\n".join(f"{i}: {line}" for i, line in enumerate(lines, 1))
    raw_claims = adapter.extract_claims(document_id=doc["document_id"], path=doc["path"], numbered_text=numbered)
    accepted: list[dict[str, Any]] = []
    rejected = 0
    for raw in raw_claims:
        candidate = _validate_llm_claim(doc, lines, raw)
        if candidate is None:
            rejected += 1
        else:
            accepted.append(candidate)
    return accepted, rejected


def analyze_workspace(workspace: str | Path, source_root: str | Path | None = None, adapter: Any = None) -> dict[str, Any]:
    workspace = Path(workspace).resolve()
    registry = json.loads((workspace / "document_registry.json").read_text(encoding="utf-8"))
    all_claims: list[dict[str, Any]] = []
    llm_rejected = 0
    extraction_mode = "deterministic"
    for doc in registry["documents"]:
        if adapter is None:
            all_claims.extend(_extract_claims(doc, workspace))
        else:
            extraction_mode = "llm_with_deterministic_evidence_validation"
            claims, rejected = _extract_llm_claims(doc, workspace, adapter)
            all_claims.extend(claims)
            llm_rejected += rejected
    groups: dict[str, list[dict[str, Any]]] = {}
    for claim in all_claims:
        if claim["subject"]:
            groups.setdefault(claim["subject"], []).append(claim)
    conflicts = []
    for subject, claims in groups.items():
        if len(claims) > 1 and len({c["polarity"] for c in claims}) > 1:
            conflicts.append({"conflict_id": "CNF-" + sha256_text(subject)[:12], "subject": subject, "claim_ids": [c["claim_id"] for c in claims], "status": "UNRESOLVED", "reason": "Opposite polarity candidates share the same normalized subject."})
    dependencies = [{"from": claim["document_id"], "to": claim["claim_id"], "type": "SUPPORTS"} for claim in all_claims]
    gaps = [{"gap_id": "GAP-" + sha256_text(claim["claim_id"])[:12], "claim_id": claim["claim_id"], "type": "HUMAN_VALIDATION_REQUIRED", "severity": "MEDIUM"} for claim in all_claims if claim["validation_status"] != "VALIDATED"]
    result = {"schema_version": "0.3", "product": "PKEA", "documents": registry["documents"], "claims": all_claims, "conflicts": conflicts, "dependencies": dependencies, "gaps": gaps, "controls": {"unsupported_claims_promoted": False, "human_gate_required": True, "canonicalization": "PROHIBITED_IN_MVP", "extraction_mode": extraction_mode, "llm_claims_rejected_by_evidence_validation": llm_rejected, "analysis_source": "INGESTED_SNAPSHOT"}}
    (workspace / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def write_report(workspace: str | Path, output: str | Path | None = None) -> Path:
    workspace = Path(workspace)
    output = Path(output or workspace / "report.md")
    data = json.loads((workspace / "analysis.json").read_text(encoding="utf-8"))
    reviews = latest_reviews(workspace)
    lines = ["# Project Knowledge & Evidence Agent — Audit Package", "", f"Documents: **{len(data['documents'])}**  ", f"Candidate claims: **{len(data['claims'])}**  ", f"Unresolved conflicts: **{len(data['conflicts'])}**  ", f"Evidence gaps: **{len(data['gaps'])}**", f"Extraction mode: **{data['controls']['extraction_mode']}**  ", f"LLM candidates rejected by evidence validation: **{data['controls']['llm_claims_rejected_by_evidence_validation']}**", "", "## Claims and evidence"]
    for claim in data["claims"]:
        e = claim["evidence"]
        review = reviews.get(claim["claim_id"])
        review_text = review["decision"] if review else "NOT_REVIEWED"
        reviewer_text = f" by `{review['reviewer']}`" if review else ""
        lines += [f"### {claim['claim_id']} — {claim['type']}", claim["text"], f"- Source: `{e['path']}` lines {e['line_start']}-{e['line_end']}", f"- Candidate status: `{claim['validation_status']}`", f"- Human review: `{review_text}`{reviewer_text}", ""]
    lines += ["## Conflicts"]
    if data["conflicts"]:
        for c in data["conflicts"]:
            lines.append(f"- `{c['conflict_id']}` — {c['subject']} — {c['status']}")
    else:
        lines.append("- None detected by the MVP rules.")
    lines += ["", "## Governance", "- No candidate is canonical by default.", "- Source locations are retained for traceability.", "- LLM output is advisory; evidence validation is deterministic.", "- Human decisions are append-only in `validation_ledger.jsonl`.", "- Conflicts remain unresolved until human review and explicit downstream resolution."]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
