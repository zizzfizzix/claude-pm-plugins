---
description: TRIGGER when: the user asks to review, improve, refactor, audit, or clean up an existing CLAUDE.md. Also trigger when the user says their CLAUDE.md is too long, noisy, or not working well with Claude Code. DO NOT TRIGGER when: no CLAUDE.md exists yet (use initiate-claude-md instead), or when the user only wants to add a single specific instruction.
---

# Refactor CLAUDE.md

## Step 1 — Read the File

Read the existing `CLAUDE.md`. If it does not exist, stop and tell the user to use the initiate-claude-md skill instead.

## Step 2 — Audit Against Best Practices

Evaluate the file on these criteria and build a numbered findings list:

**Length check**
- Count total lines. Flag if over 300 lines (critical) or over 60 lines for a small/medium project (advisory).
- Context: Claude Code consumes ~50 instruction slots itself; the CLAUDE.md budget is ~100–150 additional instructions.

**Missing sections** — flag if absent:

- WHAT (tech stack / structure)
- WHY (project purpose)
- HOW (build / test / verify commands as runnable code blocks)
- Self-learning instruction as the final line: `Update this file when you discover project conventions, preferences, or patterns worth preserving for future Claude Code sessions — keep it under 300 lines.`

**Noise to remove** (each instance is a finding):
- Code style rules or formatting preferences — belong in `.editorconfig` or formatter configs
- Linting instructions that repeat what a linter config enforces
- Overly broad directives ("always write clean code") that provide no actionable constraint
- Instructions that only apply to a specific task, not every Claude session

**Verbosity to reduce**:
- Any section longer than ~10 lines that could move to `agent_docs/`
- Duplicated guidance (same instruction stated more than once)
- Stale references to paths or commands that no longer exist

## Step 3 — Confirm Before Rewriting

Present findings to the user as a concise numbered list, then ask:

> **Audit findings (N issues):**
> 1. [finding]
> 2. [finding]
> ...
>
> Proposed actions: [brief list of what will change]
>
> Proceed with refactor?

If the user says no, show the findings report only. If the user scopes the work (e.g., "only fix 1 and 3"), respect that scope.

## Step 4 — Apply the Refactored Version

Rewrite `CLAUDE.md` addressing confirmed findings. For content moved to `agent_docs/`, create the file with the extracted content and replace the inline section with a one-line reference link.

## Step 5 — Report Changes

After writing, produce a change summary:

```
## What Changed

- Removed: [list of removed items and why]
- Added: [list of added items and why]
- Moved to agent_docs/: [files created, if any]
- Final line count: N (was M)
```

Then display the full final `CLAUDE.md` content.
