# Unified AI Operating System — Repository Registry

This registry is the controlled integration map for the GitHub repositories currently associated with `aminhardany-web`.

## Authority and runtime boundary

- `aminhardany-web/-Prompt-Operating-System` — primary AI Operating System workspace and PKEA runtime; integration hub.
- `aminhardany-web/EPKOS-Final-` — durable knowledge, governance, canonicalization and audit boundary.
- `aminhardany-web/AI-Prompt-OS` — prompt asset boundary; no independent runtime authority.
- `aminhardany-web/Evidence-Source-Matrix-` — evidence/source workstream; extraction required before integration decision.
- `aminhardany-web/Evidence-Source-Matrix-v1.1` — evidence/source workstream v1.1; extraction required before integration decision.
- `aminhardany-web/001-HUM-INT-` — separate private project; isolated until an adapter produces evidence.
- `aminhardany-web/chat-gpt-amin` — knowledge module; isolated until an adapter produces evidence.
- `aminhardany-web/data` — preserved data source; extraction is required and deletion is prohibited by the current integration mission.
- `aminhardany-web/desktop-tutorial` — tutorial source; isolated and non-runtime unless an adapter is justified.
- `aminhardany-web/OmniRoute` — forked external project; version drift and provenance must be resolved before any integration.

## Integration rule

Repositories are not physically merged merely because they are related. Source boundaries remain intact. Interoperability is provided through controlled extraction, registration, evidence mapping, dependency mapping, PKEA execution, human review and EPKOS governance.

Pipeline:

`DISCOVER → EXTRACT → REGISTER → TRACE → VALIDATE → PKEA RUNTIME → HUMAN REVIEW → EPKOS → AUDIT → RECOVERY`

The machine-readable contract is `07_System_Integration/UNIFIED_REPOSITORY_INTEGRATION_MANIFEST.json` and the adapter contract is `07_System_Integration/INTEGRATION_ADAPTER_CONTRACT.md`.

## Current integration status

| Repository | Role | Status | Next controlled action |
|---|---|---|---|
| `-Prompt-Operating-System` | Primary AI OS + PKEA | INTEGRATED | Continue runtime validation |
| `EPKOS-Final-` | Governance/knowledge | CONTROLLED_BOUNDARY | Extract/register evidence |
| `AI-Prompt-OS` | Prompt assets | CONTROLLED_BOUNDARY | Extract/register prompt assets |
| `Evidence-Source-Matrix-` | Evidence matrix | PENDING_EXTRACTION | Preserve; extract before decision |
| `Evidence-Source-Matrix-v1.1` | Evidence matrix v1.1 | PENDING_EXTRACTION | Preserve; extract before decision |
| `001-HUM-INT-` | Separate project | ISOLATED | Adapter only if evidence justifies |
| `chat-gpt-amin` | Knowledge module | ISOLATED | Extract/register via adapter |
| `data` | Data source | PRESERVE_AND_EXTRACT | Extract/register via adapter |
| `desktop-tutorial` | Tutorial source | ISOLATED | No runtime dependency unless justified |
| `OmniRoute` | Forked external project | VERSION_DRIFT_REVIEW | Resolve provenance/version before integration |

## Closure rule

No repository is deleted as part of integration. A repository can only be classified as redundant after its valuable content has been extracted, registered, traced and independently validated.

A portfolio-wide integration PASS requires every non-primary repository to be either `INTEGRATED` with evidence or `EXPLICITLY_ISOLATED` with a documented reason.
