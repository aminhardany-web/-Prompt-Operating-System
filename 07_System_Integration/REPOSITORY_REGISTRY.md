# Unified AI Operating System — Repository Registry

This registry is the single integration map for the GitHub repositories currently owned by `aminhardany-web`.

## Runtime boundary

- `aminhardany-web/-Prompt-Operating-System` — primary AI Operating System workspace and PKEA runtime; integrated package is now registered under `08_Unified_AI_OS_Final_Package`.
- `aminhardany-web/EPKOS-Final-` — durable knowledge, governance, canonicalization and audit boundary.
- `aminhardany-web/AI-Prompt-OS` — prompt-operating-system repository reserved for prompt assets; currently contains no operational README content.
- `aminhardany-web/Evidence-Source-Matrix-` — evidence/source workstream; integration target, not a runtime dependency.
- `aminhardany-web/Evidence-Source-Matrix-v1.1` — evidence/source workstream; integration target, not a runtime dependency.

## Other repositories

- `aminhardany-web/001-HUM-INT-` — separate private project; not silently merged into the runtime.
- `aminhardany-web/chat-gpt-amin` — separate private project; not silently merged into the runtime.
- `aminhardany-web/data` — separate private data repository; consumed only through an explicit future adapter.
- `aminhardany-web/desktop-tutorial` — separate private tutorial repository; no runtime dependency.

## Operating rule

Repositories are not physically merged merely because they are related. Their authoritative boundaries are preserved, while PKEA provides the project-evidence runtime and controlled interoperability.

The unified package now provides the cross-repository integration index without overwriting source material:

`Chat/Archive → Source-Exact Knowledge/Prompt Records → Master Index → Lineage/Dependency/Change Control → PKEA Evidence Runtime → Human Review → EPKOS Canonicalization`

No repository is treated as authoritative merely because it is linked from this registry. Authority remains defined by each repository's own validated baseline and evidence controls.

## Current integration status

| Repository | Role | Runtime status |
|---|---|---|
| `-Prompt-Operating-System` | Primary AI OS + PKEA | Integrated package registered; runtime evaluation pending |
| `EPKOS-Final-` | Governance/system of record | Operational candidate |
| `AI-Prompt-OS` | Prompt OS workspace | Prompt asset boundary; no independent runtime dependency |
| `Evidence-Source-Matrix-` | Evidence matrix | Separate workstream |
| `Evidence-Source-Matrix-v1.1` | Evidence matrix v1.1 | Separate workstream |
| `001-HUM-INT-` | Separate project | Isolated |
| `chat-gpt-amin` | Separate project | Isolated |
| `data` | Data repository | Isolated |
| `desktop-tutorial` | Tutorial repository | Isolated |
