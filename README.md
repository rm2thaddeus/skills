# Codex Skill Workspace

## Overview

This repository is a ready-to-run workspace for orchestrating Claude Code skills from within Cursor. It packages Anthropic's public skill references together with a curated artifact workflow so that each task starts from known patterns and ends with audit-ready outputs. Use it whenever you want an AI agent to reason about spreadsheets, documents, or presentations while keeping every intermediate deliverable in versioned storage.

Unlike a traditional Python project, this workspace centers on prompting conventions. The important code already lives in the `Code/anthropic-skills` submodule; your job (or the agent's) is to select the correct skill playbook, follow the guardrails in `.cursor/rules`, and write all generated assets into `artifacts/operations/...`.

## Repository Layout

- `Code/anthropic-skills/` – Git submodule containing the full set of Anthropic Claude skills. Every skill ships with a `SKILL.md`, example assets, and helper scripts.
- `artifacts/operations/` – Canonical archive of inputs, intermediate files, outputs, and `audit.json` logs per operation ID.
- `schemas/` – JSON Schemas for audits and manifests (see `audit.schema.json`).
- `templates/` – Ready-to-copy examples (e.g., `audit.example.json`) for new operations.
- `tools/op` – Tiny helper CLI for creating, approving, and validating operations.
- `Data Tests/` – Realistic Excel, PowerPoint, and CSV samples for dry runs or regression testing.
- `.cursor/rules/agents.mdc` – Mandatory runtime policy used by Cursor to keep agents aligned with the Phase2 proof-of-concept contract.
- `.gitmodules`, `.gitignore` – Git plumbing and workspace hygiene files.

## Quick Start

1. Clone the repository (with submodules) and open in Cursor:
   ```bash
   git clone --recurse-submodules https://github.com/your-org/codex-skill-workspace.git
   cd codex-skill-workspace
   ```
2. Inspect `.cursor/rules/agents.mdc` so your prompts stay within the approved execution model (analysis-first, non-destructive writes).
4. When the agent needs reference material, point it toward the relevant `SKILL.md` inside `Code/anthropic-skills/...`.

No additional Python environment is required unless you choose to execute one of the helper scripts bundled with the skills (for example `document-skills/xlsx/recalc.py`).

## Operation ID and Layout

- Operation ID format: `{yyyy}{mm}{dd}-{hh}{mm}{ss}-{slug}` where `{slug}` is lowercase kebab `[a-z0-9-]{1,32}`.
- Example: `20250107-143210-q4-dash-audit` → `artifacts/operations/20250107-143210-q4-dash-audit/`

Required structure:
- `input/` – Unmodified source files or metadata supplied to the agent (read-only).
- `processing/` – Scratch space for generated notes, column maps, or partially rendered assets.
- `output/` – Final deliverables (write-gated, see below).
- `audit.json` – Must validate against `schemas/audit.schema.json`.
- `provenance.json` – Checksums and tool versions; auto-created by `tools/op new`.

## Using Skills

Follow this loop whenever you run a task through the AI agent:

1. **Clarify the task** – Identify the target modality (Excel, PDF, PPTX, etc.) and open the matching `SKILL.md` for context and constraints.
2. **Confirm prerequisites** – Per the rules file, verify whether required scripts or templates exist. If a dependency is missing, surface `status: pending_implementation`.
3. **Plan with the skill guide** – Each `SKILL.md` describes supported transformations, validation requirements, and sample prompts. Use those sections to scaffold the agent's reasoning.
4. **Execute in read-first mode** – The default contract is analysis-first. Any file writes must occur in `artifacts/operations/{operation_id}/output/` and require explicit approval via write-gate.
5. **Log everything** – Capture summaries in `audit.json`, stash raw evidence under `input/` and `processing/`, and export deliverables to `output/`.
6. **Report via the output contract** – Return the JSON aligned to `schemas/audit.schema.json` fields (`status`, `artifacts`, `audit_trail`, `validation`, etc.) so downstream automation stays consistent.

## Artifacts and Audit Trail

Every operation ID inside `artifacts/operations/` mirrors the expected lifecycle:

- `input/` – Unmodified source files or metadata supplied to the agent.
- `processing/` – Scratch space for generated notes, column maps, or partially rendered assets.
- `output/` – Final deliverables (CSV summaries, PowerPoint decks, JSON manifests, HTML exports, and more).
- `audit.json` – Machine-readable log describing what changed, why, and which validations ran.

When you launch a new task, create a unique timestamped directory (the existing examples show the preferred naming scheme). All intermediate content lives here so reviewers can reconstruct the full decision trail.

## Write Gate (Mechanical Approval)

- Any write to `output/` requires the presence of `output/.approved`.
- Humans approve explicitly:
  ```bash
  echo "approved-by: <name> <UTC_ISO8601>" > artifacts/operations/<operation_id>/output/.approved
  ```
- CI should remove `.approved` after packaging artifacts to prevent accidental reuse.

## Available Skill References

Some key entry points within `Code/anthropic-skills/`:

- `document-skills/xlsx/` – Spreadsheet remediation, formula repair, LibreOffice recalc workflow.
- `document-skills/docx/` – Word processing, template preservation, OOXML manipulation.
- `document-skills/pptx/` – Presentation generation, slide templating, HTML-to-PPTX converters.
- `document-skills/pdf/` – Form extraction, structure analysis, validation routines.
- `skill-creator/` – Patterns for authoring or extending bespoke skills that fit the same artifact contract.
- `artifacts-builder/`, `webapp-testing/`, `mcp-builder/` – Specialized skills for bundling assets, testing web apps, or managing MCP integrations.

Each directory includes runnable examples, reference scripts, and the authoritative `SKILL.md` playbook. Encourage the agent to cite these documents verbatim when justifying a plan.

## Sample Data and Tests

Use the files under `Data Tests/` to rehearse workflows:

- `Dashboarding Tests/` – Excel-based dashboards suitable for formula validation scenarios.
- `Excel and Powerpoint Testing/` – Larger blended datasets (CSV, HTML exports, PPTX) to stress the end-to-end artifact pipeline.

Storing dry-run outputs in `artifacts/operations/` keeps experiments reproducible and ready for comparison against real engagements.

## Extending the Workspace

- **Add new skills** by creating sibling folders under `Code/anthropic-skills/` (or updating the submodule) and documenting them with the same `SKILL.md` format.
- **Tighten policies** by editing `.cursor/rules/agents.mdc` so Cursor enforces additional validation or approval gates.
- **Automate reporting** by scripting summarizers that read `audit.json` files and aggregate KPIs, storing the results back into `artifacts/operations/.../output/`.

Because the heavy lifting lives in the skill definitions, most enhancements only require better prompts, richer examples, or new reference artifacts—no boilerplate code rewrites.

## Support and Troubleshooting

- Submodule policy: `Code/anthropic-skills` is pinned to a specific commit. Consumers should not use `--remote` updates. Maintainers: see “Submodule Policy” below.
- When a helper script (for example `recalc.py`) is not available on the local machine, declare `validation_skipped: recalc_unavailable` per the rules file.
- Keep an eye on disk usage within `artifacts/operations/`; archive or compress older runs if you replicate large datasets.

With these patterns in place, you can drop this repository into any Codex session and have Claude Code-powered agents deliver fully auditable office-automation results from day one.

## Submodule Policy (Maintainers)

The `Code/anthropic-skills` submodule is pinned to a commit. To bump:
```bash
cd Code/anthropic-skills
git fetch
git checkout <new-commit>
cd ..
git add Code/anthropic-skills
git commit -m "chore(skills): bump submodule to <shortsha>"
```

## Offline Mode and Environment

- `.env` is optional; never committed.
- Set `OFFLINE=1` to prevent any network fetches. Agents must rely only on local assets.
- Agents must not read `.env` contents; model credentials are configured in Cursor settings.
- Forbidden patterns in logs: `api_key=`, `Authorization:`, `Bearer `.
