# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Canonical portfolio control and state machine.
- Evidence and production release gates.
- Prompt runtime evaluation gate separating registration from production authorization.
- Explicit role boundary between EPKOS, PKEA, PROMPT-OS, Prompt Bank and chat-gpt-amin.

### Changed
- Audit findings are now treated as controlled gates rather than narrative status labels.
- `COMPLETE`/`FROZEN` decisions require evidence and validation records.
