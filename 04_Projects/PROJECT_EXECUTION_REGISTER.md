# Project Execution Register — Operational Baseline

Status: OPERATIONAL PROJECT REGISTER
Date: 2026-08-22

## Purpose

This register converts the user's existing real projects and Library subjects into an execution register for the existing Prompt OS / PKEA environment.

No new architecture is introduced. No new system layer is introduced. The existing repository is used as the operational container.

Important evidence rule: a project title appearing in prior conversation history is not treated as proof that its files or complete project corpus are already present in GitHub. GitHub evidence and conversation evidence remain distinct.

## Active project corpus supplied by the user

| Project / subject | User-provided context | Operational mission | Execution focus | GitHub evidence status |
|---|---|---|---|---|
| طرح استراتژیک بنادر / طرح استراتژیک بندر امام خمینی | Recent / yesterday | Develop and consolidate the strategic planning work and its evidence base | Recover prior work, decisions, sources and current state; produce traceable strategic outputs | Not located in repository search; must be treated as external project corpus until ingested |
| Therapy Room | Aug 20; 20 members | Preserve and develop the project's existing knowledge and working material | Recover conversations/material, determine current decisions and usable outputs | Not located in repository search |
| کتاب کانتینر | Aug 20; 30 members | Develop the containerization book from existing research, drafts and conversations | Recover book structure, chapters, sources, prompts and editorial decisions | Not located in repository search |
| برنامه مالی | Aug 20 | Consolidate the financial-plan work into a usable project record and outputs | Recover assumptions, calculations, decisions and outputs | Not located in repository search |
| درک مفهوم | Aug 20; member count supplied by user | Consolidate the conceptual-learning material into reusable knowledge | Recover explanations, definitions, examples and unresolved questions | Not located in repository search |
| اوتلندر | Aug 16; 20 members | Preserve and continue the existing Outlander project material | Recover decisions, research and outputs | Not located in repository search |
| ISPS | Aug 9 | Develop the ISPS knowledge/research work | Recover sources, notes, standards, analysis and outputs | Not located in repository search |
| Book Translation Engine | Aug 2; 30 members | Develop the existing book-translation workflow/material | Recover translation prompts, terminology, source/target text and editorial decisions | Not located in repository search |
| کتابخانه مدیریت بندری | Aug 1 | Consolidate port-management knowledge into a reusable Library | Recover source documents, classifications, notes and validated knowledge | Not located in repository search |
| قوانین و مقررات مناقصات و مزایدات | Jul 1; 24 members | Consolidate tender/auction legal and regulatory knowledge | Recover authoritative texts, versions, interpretations and evidence | Not located in repository search |
| ترجمه و ویراستار | Jul 15; 20 members | Consolidate translation/editing work and reusable practices | Recover prompts, terminology, editorial rules and completed work | Not located in repository search |
| قوانین و مقررات مناقصات و قراردادها | Jan 7 | Consolidate procurement and contract regulations into a controlled knowledge base | Recover source texts, versions, interpretations and outputs | Not located in repository search |

## Existing operational assets to use

The existing repository already contains the governance layer, Prompt Library categories, workflow prompts, AI roles, tested-prompt area, templates, project/knowledge-recovery areas and the PKEA product. These existing assets are to be used as-is rather than replaced by another architecture.

PKEA's supported baseline input formats are MD/Markdown, TXT, JSON, CSV and DOCX. Its evidence model is source-first and line-traceable. Unsupported or unverified formats must not be represented as already ingested.

## Execution rule

For every project, the operational sequence is:

1. Recover the existing project corpus from the user's available Library/conversation/project material.
2. Preserve source text and provenance; do not rewrite source material during recovery.
3. Identify project decisions, prompts, sources, claims, outputs and unresolved items.
4. Place the recovered material into the existing project workspace and Prompt Library locations where appropriate.
5. Run PKEA over the supported corpus.
6. Review the resulting evidence, conflicts, dependencies and gaps.
7. Use the existing Prompt OS workflows and Prompt Bank assets to perform the actual project work.
8. Produce a human-usable output and retain its traceability to source material.

## Priority of execution

The register does not create a new architecture or a new project-management framework. Priority follows practical value and the user's existing work:

P0 — طرح استراتژیک بنادر / بندر امام خمینی
P1 — کتاب کانتینریزاسیون
P1 — ISPS
P1 — کتابخانه مدیریت بندری
P1 — قوانین و مقررات مناقصات و قراردادها / مزایدات
P2 — Book Translation Engine / ترجمه و ویراستار
P2 — برنامه مالی
P2 — Therapy Room
P2 — درک مفهوم
P2 — اوتلندر

## Completion rule

A project is not marked operational merely because a folder, prompt category or README exists. It is operational only when its real source corpus is present, provenance is preserved, PKEA can process the supported corpus, and at least one useful project output can be traced back to the source material.

## Current conclusion

The repository is the operational home for the existing system, but the user-supplied projects listed above are not evidenced as already ingested into GitHub. This register therefore records them for controlled execution without falsely claiming that their corpora are already present.
