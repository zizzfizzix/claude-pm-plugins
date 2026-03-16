# Claude Plugin Marketplace

This repository hosts a plugin marketplace for Claude Code — a catalog of plugins that extend Claude Code with custom skills, agents, hooks, and MCP servers.

## Repository Structure

```
.
├── .claude-plugin/
│   └── marketplace.json          # Marketplace catalog (required)
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       ├── skills/               # Agent skills (SKILL.md files)
│       ├── commands/             # Slash commands (Markdown files)
│       ├── agents/               # Custom agent definitions
│       ├── hooks/
│       │   └── hooks.json        # Event hooks
│       ├── .mcp.json             # MCP server configs
│       ├── .lsp.json             # LSP server configs
│       ├── settings.json         # Default plugin settings
│       └── README.md
└── CLAUDE.md
```

## Marketplace File

The marketplace catalog lives at `.claude-plugin/marketplace.json`. Every plugin entry requires `name` and `source`.

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Your Name or Team",
    "email": "contact@example.com"
  },
  "metadata": {
    "description": "Brief description of what this marketplace offers",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "What this plugin does",
      "version": "1.0.0",
      "author": { "name": "Author Name" },
      "license": "MIT",
      "category": "productivity",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

## Plugin Manifest

Each plugin needs `.claude-plugin/plugin.json`:

```json
{
  "name": "plugin-name",
  "description": "What this plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "homepage": "https://example.com/docs",
  "repository": "https://github.com/org/plugin-repo",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

## Plugin Components

### Skills

Skills live in `skills/<skill-name>/SKILL.md`. The folder name becomes the skill name (namespaced as `/plugin-name:skill-name`).

```markdown
---
description: What this skill does — Claude uses this to decide when to invoke it
disable-model-invocation: true
---

Instructions for Claude when this skill is invoked. Use $ARGUMENTS to capture user input.
```

### Commands

Commands live in `commands/` as Markdown files. Unlike skills, commands are user-invoked (not model-invoked).

### Agents

Custom agents live in `agents/` as Markdown files. Reference them in `settings.json` to set as the default agent for the plugin.

### Hooks

Hooks live in `hooks/hooks.json`. Use `${CLAUDE_PLUGIN_ROOT}` to reference scripts within the plugin.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  }
}
```

### MCP Servers

MCP server configs live in `.mcp.json` at the plugin root:

```json
{
  "server-name": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
  }
}
```

## Plugin Sources

Plugins in this marketplace can be sourced from:

| Source | Example |
|--------|---------|
| Relative path (same repo) | `"./plugins/my-plugin"` |
| GitHub repo | `{ "source": "github", "repo": "owner/repo", "ref": "v1.0.0" }` |
| Git URL | `{ "source": "url", "url": "https://gitlab.com/org/plugin.git" }` |
| Git subdirectory | `{ "source": "git-subdir", "url": "owner/monorepo", "path": "tools/plugin" }` |
| npm package | `{ "source": "npm", "package": "@org/plugin", "version": "1.0.0" }` |

Pin to a specific commit with `"sha": "<40-char-sha>"` for reproducibility.

## Development Workflow

### Add a new plugin

1. Create the plugin directory under `plugins/`:
   ```bash
   mkdir -p plugins/my-plugin/.claude-plugin
   mkdir -p plugins/my-plugin/skills/my-skill
   ```
2. Write `.claude-plugin/plugin.json` (manifest)
3. Write `skills/my-skill/SKILL.md` (or commands, agents, hooks)
4. Add the plugin entry to `.claude-plugin/marketplace.json`
5. Test locally (see below)
6. Commit and push

### Test locally

Load a single plugin directly without installing:
```bash
claude --plugin-dir ./plugins/my-plugin
```

Load multiple plugins at once:
```bash
claude --plugin-dir ./plugins/plugin-one --plugin-dir ./plugins/plugin-two
```

Reload plugins after changes without restarting:
```
/reload-plugins
```

### Validate the marketplace

```bash
claude plugin validate .
```

Or from inside Claude Code:
```
/plugin validate .
```

### Add this marketplace to Claude Code

```
/plugin marketplace add ./                    # local path
/plugin marketplace add owner/this-repo       # after pushing to GitHub
```

### Install a plugin from this marketplace

```
/plugin install plugin-name@marketplace-name
```

## Versioning

- Use [semantic versioning](https://semver.org/) in all `plugin.json` manifests
- Set version in `plugin.json` (not in the marketplace entry) for all non-relative-path plugins
- For relative-path plugins (same repo), set version only in the marketplace entry
- Each pinned ref/SHA must have a unique version — Claude Code skips updates when versions match

## Key Rules

- **Plugin directories**: `commands/`, `agents/`, `skills/`, `hooks/` go at the **plugin root**, never inside `.claude-plugin/`
- **Cross-plugin file sharing**: plugins cannot reference files outside their directory via `../`. Use symlinks if sharing is needed.
- **`${CLAUDE_PLUGIN_ROOT}`**: always use this variable in hooks and MCP configs to reference plugin-internal files
- **Reserved marketplace names**: do not use `claude-code-marketplace`, `anthropic-marketplace`, or similar official names
- **Strict mode** (`strict: true` default): `plugin.json` is authoritative for component definitions; marketplace entry supplements it

## Submitting to the Official Marketplace

To submit a plugin to Anthropic's official marketplace:
- Claude.ai: `claude.ai/settings/plugins/submit`
- Console: `platform.claude.com/plugins/submit`

## References

- [Create plugins](https://code.claude.com/docs/en/plugins)
- [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)
- [Plugin settings](https://code.claude.com/docs/en/settings#plugin-settings)
