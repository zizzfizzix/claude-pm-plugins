---
description: TRIGGER when: the user asks to create a new CLAUDE.md, initialize Claude Code instructions for a project, or set up a claude.md file from scratch. DO NOT TRIGGER when: a CLAUDE.md already exists and the user wants to improve or refactor it (use refactor-claude-md instead), or when the user is asking general questions about CLAUDE.md format.
---

# Create CLAUDE.md

## Step 1 — Explore the Project

Before writing anything, build a picture of the project:

- List the root directory contents
- Identify the tech stack: language(s), frameworks, package managers (look for `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `pom.xml`, etc.)
- Identify the build system and key commands (check `Makefile`, `scripts` in `package.json`, `justfile`, `Taskfile.yml`)
- Identify the test runner and how to run tests
- Note the key directory layout (src, tests, docs, etc.)
- Check for an existing README to understand project purpose
- Check whether a CLAUDE.md already exists — if it does, stop and tell the user to use the refactor-claude-md skill instead

## Step 2 — Clarify Purpose (if unclear)

If the project purpose is not obvious from the README or directory structure, ask the user one focused question:

> "What is this project for, and who are its main users?"

Do not ask more than one question. Proceed once you have enough to write a WHY section.

## Step 3 — Draft the CLAUDE.md

Write a CLAUDE.md that covers exactly three areas:

**WHAT** — Tech stack, key directories, architecture in 3–8 bullet points. No prose paragraphs.

**WHY** — One or two sentences on the project purpose and its users.

**HOW** — The exact commands to: build the project, run tests, run a single test, lint/typecheck, and start a dev server (omit any that don't apply). Use fenced code blocks.

Always include the following self-learning instruction as the final line of the file:

> Update this file when you discover project conventions, preferences, or patterns worth preserving for future Claude Code sessions — keep it under 300 lines.

Constraints:

- Target under 60 lines for small/medium projects; never exceed 300 lines
- Include only guidance that applies to every task in this repo
- Do not include code style rules, formatting preferences, or linting configuration
- Do not include auto-generated boilerplate or placeholder sections
- If a topic needs more than ~10 lines to explain, create an `agent_docs/<topic>.md` file and add a one-line link in CLAUDE.md instead
- Place the most critical instruction (if any) as the first line; the self-learning instruction as the last line

## Step 4 — Write the File

Write the drafted content to `CLAUDE.md` in the project root.

## Step 5 — Commit

If the working directory is a git repo, offer to commit the new file. Use Conventional Commits format — consult `agent_docs/conventional-commits.md` if it exists in the project, otherwise default to:

```
docs: add CLAUDE.md
```

Do not commit automatically — ask the user first.

## Step 6 — Verify

Read back the file you just wrote and display it to the user with a brief summary: line count, sections included, and any `agent_docs/` files created.
