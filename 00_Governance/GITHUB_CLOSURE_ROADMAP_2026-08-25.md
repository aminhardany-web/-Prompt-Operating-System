# GitHub Closure Roadmap — 2026-08-25

Status: ACTIVE — EXECUTION, NOT REPORTING
Authority: Owner/admin access verified through the connected GitHub integration.
Scope: Close the outstanding GitHub audit findings without architecture redesign, product expansion, repository merge/rename/archive/delete, or creation of a second custom GitHub App/Bot.

## Non-negotiable execution rule
A checkbox is complete only when direct evidence exists. Repository metadata, README claims, or an earlier assistant statement are not evidence of runtime/security closure.

## Canonical boundaries
- `aminhardany-web/-Prompt-Operating-System`: operational PROMPT-OS/PKEA source of truth.
- `aminhardany-web/EPKOS-Final-`: durable EPKOS governance/knowledge boundary.
- `aminhardany-web/chat-gpt-amin`: ChatGPT-facing knowledge/runtime module.
- `aminhardany-web/AI-Prompt-OS`: compatibility boundary, not a second source of truth.
- `aminhardany-web/OmniRoute`: independent external/Forked AI gateway; do not merge into the core architecture during this closure.

## Closure checklist
- [ ] PROMPT-OS/PKEA: obtain and verify a real GitHub Actions PASS on the current operational source.
- [ ] PKEA runtime: execute existing smoke/test path and record PASS/FAIL evidence.
- [ ] chat-gpt-amin: execute existing Python/web CI and real end-to-end runtime verification.
- [ ] Repository security: directly verify Secret Scanning/Secret Protection, Push Protection, Dependabot, and Code Scanning/CodeQL where available.
- [ ] Branch protection: directly verify/configure protection for canonical operational/governance branches without architectural change.
- [ ] OmniRoute Fork: verify upstream/Fork relationship, run existing CI/security checks, then perform an isolated runtime smoke test.
- [ ] OmniRoute CodeQL: resolve Default Setup vs Advanced Setup so there is one non-conflicting security configuration.
- [ ] `data`: inspect purpose/content/security and remediate only confirmed problems.
- [ ] `001-HUM-INT-`: inspect structure/secrets/dependencies/workflows and remediate only confirmed problems.
- [ ] Empty Evidence-Source-Matrix repositories: keep non-authoritative/HOLD; do not invent content or duplicate sources.
- [ ] `desktop-tutorial`: leave inactive; no work unless a concrete purpose is established.
- [ ] Update the audit record and Issue #5 with direct evidence for every completed item.
- [ ] Close Issue #5 only after all applicable items are evidenced.

## Execution order
1. Trigger/verify existing PROMPT-OS CI.
2. Verify PKEA runtime.
3. Verify chat-gpt-amin CI/E2E.
4. Verify and remediate GitHub security controls.
5. Verify/configure branch protection.
6. Verify and smoke-test OmniRoute independently.
7. Close data/HUM-INT findings.
8. Final evidence audit and only then closure.

## Honesty boundary
Current state must remain PARTIALLY READY until the above evidence exists. No ZERO-GAP, FULLY VERIFIED, PRODUCTION READY, or SECURITY CLOSED claim is permitted before direct evidence is recorded.

## Tracking
Primary execution issue: GITHUB-CLOSURE-001 — Issue #5.
Previous audit: `00_Governance/GITHUB_RUNTIME_AUDIT_2026-08-25.md`.
