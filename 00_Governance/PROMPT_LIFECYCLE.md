# Prompt Lifecycle

Status: ACTIVE

Canonical lifecycle:

`CANDIDATE → REGISTERED → REVIEWED → RUNTIME_TESTED → RELEASED → DEPRECATED → ARCHIVED`

Rules:
- `REGISTERED` means identity and source traceability are established; it does not mean quality is proven.
- `REVIEWED` means a human review decision exists.
- `RUNTIME_TESTED` requires a recorded executable evaluation with PASS/FAIL.
- `RELEASED` requires runtime PASS and no unresolved blocking dependency.
- `DEPRECATED` prevents new production use but preserves history.
- `ARCHIVED` is retained for provenance and is not an active asset.

Illegal shortcut: `REGISTERED → RELEASED`.
