# ChatGPT Knowledge Module Registry

**Status:** ACTIVE SPECIFICATION
**Updated:** 2026-08-23

## Module

**Module ID:** KMOD-PORT-MARITIME-001
**Canonical Name:** chat-gpt-amin
**Role:** Port & Maritime domain knowledge and decision-support layer
**Canonical Repository:** `aminhardany-web/chat-gpt-amin`
**System Layer:** Domain Knowledge Module

## Authority chain

`EPKOS (governance/evidence) → PROMPT-OS (execution/lifecycle) → chat-gpt-amin (Port & Maritime domain knowledge) → project-specific routing (e.g. KD-003) → ChatGPT runtime`

## Supported semantic invocations

`chat-gpt-amin`
`chat-gpt-amin strategy`
`chat-gpt-amin KD-003`
`chat-gpt-amin contracts`
`chat-gpt-amin operations`
`chat-gpt-amin digital-port`
`chat-gpt-amin research`
`chat-gpt-amin translate`

## Required invocation behaviour

1. Identify the active project/context.
2. Select only relevant domain modules.
3. Load/retrieve applicable canonical sources available to the runtime.
4. Check current official sources for time-sensitive claims.
5. Separate verified facts, evidence-based inference, hypotheses and analytical opinions.
6. Preserve source/locator/version where available.
7. Route outputs to the active project baseline where applicable.
8. Never imply automatic access to historical chats or GitHub files unless the runtime actually exposes them.

## Integration states

- **Specification:** ACTIVE
- **Semantic routing:** ACTIVE
- **Repository linkage:** REGISTERED
- **Cross-repository documentation:** ACTIVE
- **Live end-to-end ChatGPT runtime injection:** NOT PROVEN
- **EPKOS/PROMPT-OS/Prompt Bank end-to-end execution test:** PENDING

## Acceptance test for full integration

Full runtime integration may only be declared after a live test proves:

`ChatGPT project/page → invoke chat-gpt-amin → retrieve canonical knowledge → route to correct module → apply evidence rules → produce traceable output → record execution/result.`

Until that test passes, the correct status is `ACTIVE SPECIFICATION / RUNTIME NOT PROVEN`, not `FULLY INTEGRATED`.
