# CLAUDE.md — claude-pm-plugins

This file documents the repository structure, conventions, and workflows for Claude Code instances working in this repo.

---

## Repository Overview

`claude-pm-plugins` is a **Claude Code plugin marketplace** — a monorepo of independently versioned plugins for Product Management workflows. Each plugin lives under `plugins/<plugin-name>/` and is distributed as a standalone Claude Code plugin.

---

## Repository Structure

```
claude-pm-plugins/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace registry (all plugins)
├── .github/
│   └── workflows/
│       └── release.yml           # Release Please GitHub Action
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest (name, version, description)
│       ├── commands/             # Slash commands (optional)
│       ├── skills/               # Skills (optional)
│       ├── agents/               # Agent definitions (optional)
│       ├── hooks/                # Hook scripts (optional)
│       └── README.md
├── .release-please-manifest.json # Release Please version manifest
├── release-please-config.json    # Release Please configuration
└── CLAUDE.md                     # This file
```

---

## Plugin Structure

Each plugin under `plugins/<plugin-name>/` follows this structure:

### `.claude-plugin/plugin.json` (required)
```json
{
  "name": "<plugin-name>",
  "version": "0.1.0",
  "description": "Short description of the plugin",
  "author": "Author Name"
}
```

### Plugin Components

| Directory   | Purpose                                            |
| ----------- | -------------------------------------------------- |
| `commands/` | Slash commands invokable via `/<command-name>`     |
| `skills/`   | Skills invokable by Claude when descriptions match |
| `agents/`   | Specialized sub-agent definitions                  |
| `hooks/`    | Event hooks (pre/post tool use, etc.)              |

---

## Dev Workflow

1. Create plugin directory: `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json` with `"version": "0.1.0"`
3. Implement plugin components (commands, skills, agents, hooks)
4. Add entry to `release-please-config.json` (see Versioning section)
5. Add entry to `.release-please-manifest.json`
6. Add entry to `.claude-plugin/marketplace.json`
7. Commit as `feat(<plugin-name>): initial plugin implementation`

---

## Existing Plugins

| Plugin            | Path                         | Version | Description                                           |
| ----------------- | ---------------------------- | ------- | ----------------------------------------------------- |
| meeting-summarize | `plugins/meeting-summarize/` | 0.0.0   | Summarizes meeting notes into structured PM artefacts |

---

## Versioning and Release Process

This repo uses [Release Please](https://github.com/googleapis/release-please) to automate plugin versioning via **Conventional Commits**.

### How It Works

1. Developer pushes commits to `main` using Conventional Commit format
2. Release Please GitHub Action (`.github/workflows/release.yml`) detects commits and opens/updates a Release PR
3. The Release PR bumps versions in `plugin.json` and `.release-please-manifest.json`
4. When the Release PR is merged, Release Please creates a GitHub Release and git tag (e.g. `meeting-summarize-v1.2.0`)

### Conventional Commits

| Commit type               | Version bump            | Example                                                |
| ------------------------- | ----------------------- | ------------------------------------------------------ |
| `feat(<plugin>): ...`     | minor (0.x.0 → 0.x+1.0) | `feat(meeting-summarize): add action items extraction` |
| `fix(<plugin>): ...`      | patch (0.0.x → 0.0.x+1) | `fix(meeting-summarize): handle empty transcript`      |
| `feat(<plugin>)!: ...`    | major (x.0.0 → x+1.0.0) | `feat(meeting-summarize)!: redesign output format`     |
| `chore: ...`              | none                    | `chore: update dependencies`                           |
| `docs: ...`               | none                    | `docs: update CLAUDE.md`                               |
| `refactor(<plugin>): ...` | none                    | `refactor(meeting-summarize): extract helper`          |

The **scope** (the part in parentheses) must match the plugin's `component` value in `release-please-config.json`.

### Release Please Config Files

| File                            | Purpose                                                                 |
| ------------------------------- | ----------------------------------------------------------------------- |
| `release-please-config.json`    | Declares which packages Release Please manages and how                  |
| `.release-please-manifest.json` | Tracks current released version per package (managed by Release Please) |

**Version authority:** `plugin.json` is the authoritative version file for a plugin. Release Please updates it automatically via `extra-files` config. Do not manually edit `.release-please-manifest.json` except when adding a new plugin.

### Adding a New Plugin

When adding `plugins/<plugin-name>/`:

1. Create `plugins/<plugin-name>/.claude-plugin/plugin.json` with `"version": "0.1.0"`

2. Add plugin content (commands, skills, agents, hooks)

3. Add entry to `release-please-config.json` under `packages`:
   ```json
   "plugins/<plugin-name>": {
     "release-type": "simple",
     "component": "<plugin-name>",
     "extra-files": [
       { "type": "json", "path": ".claude-plugin/plugin.json", "jsonpath": "$.version" }
     ]
   }
   ```
   > `path` in `extra-files` is relative to the package root (`plugins/<plugin-name>/`).

4. Add `"plugins/<plugin-name>": "0.1.0"` to `.release-please-manifest.json`

5. Add entry to `.claude-plugin/marketplace.json` plugins array:
   ```json
   {
     "name": "<plugin-name>",
     "version": "0.1.0",
     "description": "...",
     "source": "./plugins/<plugin-name>"
   }
   ```

6. Commit all changes as `feat(<plugin-name>): initial plugin implementation`

### Version Management Rules

- **`plugin.json`** — authoritative version source; updated automatically by Release Please
- **`.release-please-manifest.json`** — managed by Release Please; only edit manually when first registering a plugin
- **`marketplace.json`** — must be kept in sync manually after each release; update the `version` field to match the new release

---

## Key Rules

- Each plugin is **independently versioned** — a release for one plugin does not affect others
- Use the plugin name as the **commit scope** to target the correct package
- Tags follow the pattern `<plugin-name>-v<semver>` (e.g. `meeting-summarize-v1.2.0`) due to `include-component-in-tag: true`
- `docs:` and `chore:` commits do **not** trigger releases
- Breaking changes require `!` suffix on the commit type (e.g. `feat!:` or `fix!:`)

---

## Marketplace Registry

`.claude-plugin/marketplace.json` is the central registry listing all available plugins. It is consumed by tooling that discovers and installs plugins.

Schema:
```json
{
  "name": "claude-pm-plugins",
  "owner": { "name": "..." },
  "metadata": {
    "description": "...",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "<plugin-name>",
      "version": "<current-version>",
      "description": "...",
      "source": "./plugins/<plugin-name>"
    }
  ]
}
```

Update `marketplace.json` manually after each plugin release to keep versions in sync.

---

## Plugin Submission

To submit a new plugin to the marketplace, open a PR with:
- The plugin directory under `plugins/<plugin-name>/`
- Updated `release-please-config.json`, `.release-please-manifest.json`, and `marketplace.json`
- A `feat(<plugin-name>): initial plugin implementation` commit

See the [Contributing Guide](CONTRIBUTING.md) if it exists, or open an issue for guidance.
