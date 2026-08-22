# PROMPT BANK RE-AUDIT — 2026-08-23

## Executive status
The historical Prompt Bank is larger than the page-level 15-prompt intake previously audited.

Current evidence-bound counts from Prompt Bank v3.1:
- Canonical source records: 530
- Legacy exact-source records: 509
- Structural promotions: 21
- Deep Scan candidates outside canonical: 205
- Runtime-tested canonical records: 0
- Fully semantic-validated canonical records: 0
- Global historical recall: OPEN

## Source coverage
The archive-derived exact-source corpus is available in the connected Library as:
`PROMPT_BANK_EXACT_SOURCE_v1.0.jsonl`

The current management index is:
`PROMPT_BANK_MASTER_INDEX_v3.1.csv`

The system explicitly separates:
1. exact source capture,
2. discovery candidates,
3. semantic validation,
4. runtime validation,
5. canonical promotion,
6. production release.

## Page audit reconciliation
The page-level Prompt-OS audit identified:
- 22 prompt-bearing occurrences
- 15 distinct prompt families
- 7 duplicate occurrences
- 6 baseline/container messages excluded from Prompt count

Those 15 are a controlled page-intake set only. They are not the whole historical Prompt Bank.

## Validation boundary
No prompt is considered runtime-tested or production-released merely because it exists in the source corpus or management index. Current test registry shows runtime status NOT_TESTED and release NOT_RELEASED for the canonical corpus.

## Historical recall boundary
A separate re-audit found 537 user messages containing lexical prompt references, 496 distinct texts, 461 exact matches already covered in the 509-record legacy bank, 35 distinct texts not exactly present, and 59 messages remaining in an explicit prompt-reference/candidate queue. These are not all guaranteed to be prompts; semantic classification remains open.

## GitHub persistence boundary
GitHub contains the Prompt-OS governance/control structure and current synchronization/audit manifests. The full 509-record exact-source JSONL has not been mirrored into GitHub as individual prompt files in this commit because the connected Library remains the source corpus of record. This is intentional and must not be described as a completed full GitHub text mirror.

## Rule
Never infer "registered" from "mentioned", "retrieved", "similar", or "present in memory". Exact source registration requires prompt text + provenance + persistent record.
