# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## What This Repo Is

A monorepo of independently versioned Claude Code plugins for Product Management workflows. Each plugin lives under `plugins/<plugin-name>/` and is distributed standalone.

---

## Plugin Structure

Each plugin contains:

- `.claude-plugin/plugin.json` — manifest with `name`, `version`, `description`, `author`
- `commands/` — slash commands
- `skills/` — skills invokable by Claude; name them short (e.g. `initiate`, `refactor`) since invocation is prefixed with the plugin name (`<plugin-name>:<skill-name>`)
- `agents/` — sub-agent definitions
- `hooks/` — event hooks
- `scripts/` — helper scripts (e.g. transcript cleaners)

---

## Adding a New Plugin

1. Create `plugins/<plugin-name>/.claude-plugin/plugin.json` with `"version": "0.1.0"`
2. Add plugin content (commands, skills, agents, hooks)
3. Register in `release-please-config.json` under `packages` (use existing entry as template)
4. Add `"plugins/<plugin-name>": "0.1.0"` to `.release-please-manifest.json`
5. Add entry to `.claude-plugin/marketplace.json` plugins array
6. Commit as `feat(<plugin-name>): initial plugin implementation`

---

## Versioning

Uses [Release Please](https://github.com/googleapis/release-please) with Conventional Commits. The commit **scope must match** the plugin's `component` in `release-please-config.json`.

| Commit prefix          | Version bump |
| ---------------------- | ------------ |
| `feat(<plugin>):`      | minor        |
| `fix(<plugin>):`       | patch        |
| `feat(<plugin>)!:`     | major        |
| `chore:` / `docs:`     | none         |

See [agent_docs/conventional-commits.md](agent_docs/conventional-commits.md) for full commit message format, type reference, and PR title/description guidelines.

**Version authority:** `plugin.json` is the source of truth. After each release, manually update the matching `version` in `.claude-plugin/marketplace.json`.

---

## Key Rules

- Tags follow `<plugin-name>-v<semver>` (e.g. `meeting-summarize-v1.2.0`)
- Never manually edit `.release-please-manifest.json` except when first registering a plugin
- Each plugin is independently versioned — releasing one does not affect others
