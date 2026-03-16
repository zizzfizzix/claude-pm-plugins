#!/usr/bin/env python3
"""
clean-transcript.py — Strip formatting artifacts from meeting transcripts.

Supported formats:
  .srt   SubRip        — sequence number + timestamp + text
  .vtt   WebVTT        — WEBVTT header + cue timestamps + text
  .tsv   Zoom/Teams    — tab-separated: start, end, speaker, text
  .txt   Plain text    — lightly cleaned, timestamps removed
  .md    Markdown      — markdown stripped, then plain-text cleaned

Output: cleaned dialogue to stdout, speaker labels preserved.
"""

import sys
import re
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Format-specific cleaners
# ---------------------------------------------------------------------------

def clean_srt(text: str) -> str:
    """Remove SRT sequence numbers and timestamp lines."""
    lines = text.splitlines()
    result = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        # Bare integer — sequence number
        if re.fullmatch(r"\d+", s):
            continue
        # Timestamp: 00:00:01,000 --> 00:00:04,000  (with optional position tags)
        if re.match(r"\d{2}:\d{2}:\d{2}[,\.]\d{3}\s*-->", s):
            continue
        result.append(s)
    return "\n".join(result)


def clean_vtt(text: str) -> str:
    """Remove WebVTT header, cue identifiers, and timestamp lines."""
    lines = text.splitlines()
    result = []
    past_header = False
    i = 0
    while i < len(lines):
        s = lines[i].strip()

        # Skip the WEBVTT signature block and NOTE sections
        if not past_header:
            if re.match(r"^WEBVTT|^NOTE\b|^STYLE\b|^REGION\b", s, re.IGNORECASE) or not s:
                i += 1
                continue
            past_header = True

        if not s:
            i += 1
            continue

        # Timestamp line: 00:00.000 --> 00:00.000  or  00:00:00.000 --> ...
        if re.match(r"[\d:]+\.\d{3}\s*-->", s):
            i += 1
            continue

        # Cue identifier — a non-timestamp line immediately before a timestamp
        next_nonempty = next(
            (lines[j].strip() for j in range(i + 1, len(lines)) if lines[j].strip()),
            ""
        )
        if re.match(r"[\d:]+\.\d{3}\s*-->", next_nonempty):
            i += 1
            continue

        result.append(s)
        i += 1

    return "\n".join(result)


def clean_tsv(text: str) -> str:
    """Parse TSV transcripts (Zoom, Teams, Otter.ai export formats).

    Supported column layouts:
      4-col: start  end  speaker  text
      3-col: start  speaker  text
      2-col: speaker  text
    """
    result = []
    for line in text.splitlines():
        parts = [p.strip() for p in line.split("\t")]
        if len(parts) >= 4:
            speaker, dialogue = parts[2], parts[3]
        elif len(parts) == 3:
            speaker, dialogue = parts[1], parts[2]
        elif len(parts) == 2:
            speaker, dialogue = parts[0], parts[1]
        else:
            result.append(line.strip())
            continue
        if speaker:
            result.append(f"{speaker}: {dialogue}")
        else:
            result.append(dialogue)
    return "\n".join(result)


def clean_md(text: str) -> str:
    """Strip markdown formatting, then apply plain-text cleaning."""
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*{1,3}([^*\n]+)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}([^_\n]+)_{1,3}", r"\1", text)
    text = re.sub(r"`([^`\n]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    return clean_txt(text)


def clean_txt(text: str) -> str:
    """Remove bare timestamp lines from plain-text transcripts."""
    result = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        # Skip bare timestamps like "1:23" or "01:23:45 PM"
        if re.fullmatch(r"\d{1,2}:\d{2}(:\d{2})?(\s*[ap]m)?", s, re.IGNORECASE):
            continue
        result.append(s)
    return "\n".join(result)


# ---------------------------------------------------------------------------
# Post-processing
# ---------------------------------------------------------------------------

def merge_consecutive_speaker(text: str) -> str:
    """Merge consecutive lines from the same speaker into one paragraph."""
    lines = text.splitlines()
    result = []
    current_speaker: str | None = None
    current_lines: list[str] = []

    def flush():
        if not current_lines:
            return
        content = " ".join(current_lines)
        if current_speaker:
            result.append(f"{current_speaker}: {content}")
        else:
            result.append(content)

    for line in lines:
        s = line.strip()
        if not s:
            flush()
            current_speaker = None
            current_lines = []
            continue

        # Detect "Speaker Name: dialogue" pattern (name ≤ 40 chars, no newlines)
        m = re.match(r"^([A-Za-z][^:\n]{0,39}):\s+(.+)$", s)
        if m:
            speaker, dialogue = m.group(1).strip(), m.group(2).strip()
            if speaker == current_speaker:
                current_lines.append(dialogue)
            else:
                flush()
                current_speaker = speaker
                current_lines = [dialogue]
        else:
            # Continuation or no speaker label
            current_lines.append(s)

    flush()
    return "\n".join(result)


def remove_duplicate_lines(text: str) -> str:
    """Drop exact duplicate consecutive lines (common in auto-captions)."""
    lines = text.splitlines()
    result = []
    prev = None
    for line in lines:
        if line != prev:
            result.append(line)
        prev = line
    return "\n".join(result)


# ---------------------------------------------------------------------------
# Format detection
# ---------------------------------------------------------------------------

def detect_format(path: Path | None, content: str) -> str:
    if path:
        ext = path.suffix.lower()
        if ext == ".srt":
            return "srt"
        if ext == ".vtt":
            return "vtt"
        if ext in (".tsv", ".csv"):
            return "tsv"
        if ext == ".md":
            return "md"

    # Content sniffing
    first_lines = content[:500]
    if first_lines.lstrip().startswith("WEBVTT"):
        return "vtt"
    if re.search(r"^\d+\s*\n\d{2}:\d{2}:\d{2},\d{3}\s*-->", first_lines, re.MULTILINE):
        return "srt"
    if "\t" in (content.splitlines()[0] if content.splitlines() else ""):
        return "tsv"
    return "txt"


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

_CLEANERS = {
    "srt": clean_srt,
    "vtt": clean_vtt,
    "tsv": clean_tsv,
    "md":  clean_md,
    "txt": clean_txt,
}


def clean(content: str, fmt: str) -> str:
    cleaned = _CLEANERS.get(fmt, clean_txt)(content)
    cleaned = merge_consecutive_speaker(cleaned)
    cleaned = remove_duplicate_lines(cleaned)
    return cleaned.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Clean meeting transcript files — strips timestamps and formatting."
    )
    parser.add_argument(
        "file", nargs="?",
        help="Transcript file path (reads stdin if omitted)"
    )
    parser.add_argument(
        "--format", choices=list(_CLEANERS),
        help="Force format (auto-detected from extension/content if omitted)"
    )
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        content = sys.stdin.read()
        path = None

    fmt = args.format or detect_format(path, content)
    print(clean(content, fmt))


if __name__ == "__main__":
    main()
