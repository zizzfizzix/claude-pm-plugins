# Conventional Commits Guide

## Commit message format

```
<type>(<scope>): <summary>

[optional body]

[optional footer(s)]
```

- **type** — what kind of change (see table below)
- **scope** — plugin name for plugin-scoped changes (e.g. `meeting-summarize`); omit for repo-wide changes
- **summary** — imperative mood, lowercase, no trailing period; entire first line ≤ 72 chars
- **body** — optional, free-form; explains *why*, not *what*
- **breaking change** — append `!` after scope (`feat(my-plugin)!:`) and add a `BREAKING CHANGE: <description>` footer

## Type reference

| Type       | When to use                                      |
| ---------- | ------------------------------------------------ |
| `feat`     | New feature or capability                        |
| `fix`      | Bug fix                                          |
| `docs`     | Documentation only (no code change)              |
| `chore`    | Maintenance, dependency updates, config changes  |
| `refactor` | Code restructure with no behaviour change        |
| `test`     | Adding or fixing tests                           |
| `perf`     | Performance improvement                          |
| `ci`       | CI/CD pipeline changes                           |

## Examples

```
feat(meeting-summarize): add export-to-notion command
fix(claude-md): handle missing CLAUDE.md gracefully
docs: add conventional commits guide
chore: upgrade release-please to v4
feat(retro-facilitator)!: redesign output schema

BREAKING CHANGE: output JSON shape changed; consumers must update parsers
```

## PR titles

PR titles **must** follow the same `type(scope): summary` format. Release Please reads the PR title when squash-merging to determine the version bump — an incorrectly formatted title breaks automated versioning.

## PR descriptions

Include these three sections:

```markdown
## What
[Brief description of the change]

## Why
[Motivation or linked issue — e.g. "Fixes #42"]

## Testing
[How the change was verified — manual steps, test commands, or "N/A"]
```
