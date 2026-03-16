---
description: Clean and summarize a meeting transcript. Accepts .srt, .vtt, .tsv, .txt, or .md files — auto-detects format, strips timestamps, then produces a structured summary matched to the meeting type.
argument-hint: <path-to-transcript>
---

# Meeting Summarize

Transcript to process: **$ARGUMENTS**

## Phase 1 — Clean the Transcript

Run the cleanup script to strip timestamps, sequence numbers, cue identifiers, and formatting artifacts:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/clean-transcript.py" "$ARGUMENTS"
```

Capture the full stdout output. This is the **cleaned transcript**.

If the file does not exist, tell the user and stop.

## Phase 2 — Analyse and Summarise

Pass the cleaned transcript to the **meeting-analyzer** agent with this prompt:

> Here is the cleaned transcript. Detect the meeting type, then produce a structured summary using the matching template.
>
> ---
>
> [paste cleaned transcript here]

## Phase 3 — Present Results

Output the agent's summary directly to the user with no additional commentary.
