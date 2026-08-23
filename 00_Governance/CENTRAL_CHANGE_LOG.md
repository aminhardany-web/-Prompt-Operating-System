# Central Change Log

Status: ACTIVE

Only changes that alter a frozen baseline, authority boundary, lifecycle state, dependency rule, or release gate belong here.

| Date | Change | Reason | Evidence/Commit | Authority |
|---|---|---|---|---|
| 2026-08-23 | Added executable PKEA verification workflow | Convert stated verification requirement into repository-executable evidence | `pkea-ci.yml` | Repository admin |
| 2026-08-23 | Added prompt runtime evaluation gate | Prevent registration from being mistaken for runtime validation | `PROMPT_RUNTIME_EVALUATION.md` | PROMPT-OS governance |
| 2026-08-23 | Added dependency registry | Make cross-project dependencies explicit and auditable | `DEPENDENCY_REGISTRY.md` | EPKOS boundary |

No entry in this log may be used to claim that an independent audit has passed. It records changes; it does not replace verification evidence.
