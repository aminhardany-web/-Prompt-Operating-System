# AI Content Team OS

Implementation of the supplied seven-agent content pipeline as a controlled module of the Prompt Operating System.

## Current state
**INITIALIZED — CONFIGURATION GATE OPEN**

Created:
- `CLAUDE.md`
- seven agent specifications under `.claude/agents/`
- brand voice and swipe-file stores
- ideas inbox
- content calendar
- performance tracker

The runtime is intentionally paused before research because the supplied system requires five user-specific inputs: niche, audience, brand voice, CTA style, and this week's content objective.

## Approval gates
1. Ideas require Editor-in-Chief approval before scripting.
2. Finished draft requires Editor-in-Chief approval before staging/publishing.
3. Publishing requires explicit `go`.
4. Analytics conclusions require real performance data.
