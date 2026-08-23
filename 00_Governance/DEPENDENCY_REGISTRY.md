# Dependency Registry

Status: ACTIVE / CONTROLLED
Effective: 2026-08-23

This registry records cross-asset dependencies without creating a second architecture.

| Upstream | Downstream | Dependency | Evidence required | State |
|---|---|---|---|---|
| EPKOS | PKEA | Governance/authority boundary | EPKOS baseline + PKEA baseline | VERIFIED |
| PROMPT-OS | Prompt Bank | Prompt asset lifecycle | Prompt Library + runtime evaluation record | CONTROLLED |
| PKEA | EPKOS | Candidate evidence handoff | Human validation + canonicalization record | NOT-AUTOMATIC |
| RA-001 | KD-003 | Reference architecture context | Frozen RA-001 reference | CONTROLLED |
| WP2 | KD-003 | Fact-base dependency | Source-backed data package | BLOCKED-UNTIL-SUPPLIED |

Rules:
- A dependency is not satisfied by a narrative statement alone.
- `BLOCKED-UNTIL-SUPPLIED` must not be silently promoted.
- Architecture changes require a separate controlled-change record.
