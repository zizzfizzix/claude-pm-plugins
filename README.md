# claude-pm-plugins

A monorepo of independently versioned [Claude Code](https://claude.ai/code) plugins for Product Management workflows.

## Plugins

| Plugin                                            | Version | Description                                                                                                                                         |
| ------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| [meeting-summarize](./plugins/meeting-summarize/) | 1.0.0   | Clean and summarize meeting transcripts from SRT, VTT, TSV, TXT, and MD formats. Detects meeting type and applies the appropriate summary template. |
| [claude-md](./plugins/claude-md/)                 | 1.0.0   | Create and refactor CLAUDE.md project instruction files following best practices for minimal, high-signal Claude Code guidance.                     |

## Plugin Details

### meeting-summarize

Processes meeting transcripts in three phases:

1. **Clean** — Strips timestamps, sequence numbers, and formatting artifacts from SRT, VTT, TSV, TXT, and MD files
2. **Analyze** — Detects meeting type (standup, demo, decision, retro, 1:1, all-hands, brainstorm) and generates a structured summary
3. **Present** — Returns a markdown summary with sections tailored to the meeting type

**Usage:** `/meeting-summarize <path-to-transcript>`

---

### claude-md

Two skills for managing CLAUDE.md project instruction files:

- **`claude-md:initiate`** — Creates a new CLAUDE.md from scratch by exploring your project structure and asking one clarifying question
- **`claude-md:refactor`** — Audits and improves an existing CLAUDE.md, trimming noise and moving long content to `agent_docs/`

Both skills target concise, high-signal output (<60 lines for most projects).

## Installation

Add this marketplace to Claude Code:

```sh
/plugin marketplace add zizzfizzix/claude-pm-plugins
```

Then install individual plugins:

```sh
/plugin install meeting-summarize
/plugin install claude-md
```

## Repository Structure

```text
claude-pm-plugins/
├── .claude-plugin/
│   └── marketplace.json          # central plugin registry
├── plugins/
│   ├── meeting-summarize/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json       # manifest: name, version, description, author
│   │   ├── agents/
│   │   │   └── meeting-analyzer.md
│   │   ├── commands/
│   │   │   └── meeting-summarize.md
│   │   └── scripts/
│   │       └── clean-transcript.py
│   └── claude-md/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           ├── initiate.md
│           └── refactor.md
├── release-please-config.json
├── .release-please-manifest.json
└── CLAUDE.md
```

Each plugin follows the same layout:

```text
<plugin-name>/
├── .claude-plugin/
│   └── plugin.json     # manifest: name, version, description, author
├── commands/           # slash commands
├── skills/             # skills invokable as <plugin-name>:<skill-name>
├── agents/             # sub-agent definitions
├── hooks/              # event hooks
└── scripts/            # helper scripts
```

## Adding a New Plugin

1. Create `plugins/<plugin-name>/.claude-plugin/plugin.json` with `"version": "0.1.0"`
2. Add plugin content (commands, skills, agents, hooks)
3. Register in `release-please-config.json` under `packages`
4. Add `"plugins/<plugin-name>": "0.1.0"` to `.release-please-manifest.json`
5. Add an entry to `.claude-plugin/marketplace.json`
6. Commit as `feat(<plugin-name>): initial plugin implementation`

## Versioning

Uses [Release Please](https://github.com/googleapis/release-please) with [Conventional Commits](https://www.conventionalcommits.org/). Each plugin is independently versioned.

| Commit prefix      | Version bump |
| ------------------ | ------------ |
| `feat(<plugin>):`  | minor        |
| `fix(<plugin>):`   | patch        |
| `feat(<plugin>)!:` | major        |
| `chore:` / `docs:` | none         |

Tags follow the format `<plugin-name>-v<semver>` (e.g. `meeting-summarize-v1.2.0`).

## License

MIT — see [LICENSE](./LICENSE)
