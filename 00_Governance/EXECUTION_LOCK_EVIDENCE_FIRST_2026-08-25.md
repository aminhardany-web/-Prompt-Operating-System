# EXECUTION LOCK — EVIDENCE-FIRST DEFECT REMEDIATION

Status: LOCKED
Mode: EXECUTE → VERIFY → DOCUMENT

This is the governing execution instruction for remediation work in this project/repository.

- Do not report a defect as resolved without direct GitHub/runtime evidence.
- Reproduce/check every defect, fix the actual cause, execute verification, record evidence, then resolve it.
- If the available GitHub/OpenAI tooling cannot perform a required action, record BLOCKED and state the exact missing permission/action. Never simulate completion.
- Never claim PASS, READY, ACTIVE, CONNECTED, SECURE, or CLOSED from metadata, README text, intended configuration, or an unexecuted workflow.
- Do not create false Bot/App/API connectivity claims.
- Do not redesign, expand, merge, rename, delete, or introduce architecture unless separately authorized.
- Preserve the existing canonical architecture and repository boundaries.
- Security controls require direct verification.
- CI failures must be fixed and rerun.
- Keep an auditable record for every remediation item.

Closure domains: PROMPT-OS/PKEA CI/runtime; chat-gpt-amin E2E; repository security controls; branch protection; OmniRoute fork/CI/security/runtime; CodeQL consistency; data repository review; 001-HUM-INT- review; evidence-matrix status; governance synchronization.

Definition of Done: zero applicable unresolved defects, or an evidenced BLOCKED state with the exact external action required from the user. Narrative-only closure is prohibited.
