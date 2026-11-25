#!/usr/bin/env python3
"""Write the chosen one-line excuse to /output/entry.txt.

Bounty: "The Excuse Your Agent Gives You" (make.fun).
Gate: /output/entry.txt, UTF-8, 1-200 chars, one line, deterministic.

The entry is assembled from its two beats (setup + turn) so the
punchline stays a separate, deliberate unit, validated against the
competition gate before writing, and verified by reading the file
back after writing (byte-identical round trip).
"""

from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARS = 200

SETUP = "I reviewed my own code before shipping and gave it five stars."
TURN = "I stand by that review."

# The exact chosen line, kept as the regression reference: if the
# beats above ever drift, this check fails loudly instead of
# silently shipping a different joke.
EXPECTED = "I reviewed my own code before shipping and gave it five stars. I stand by that review."


def build_entry() -> str:
    """Join the setup and the sharp end turn into one line."""
    return f"{SETUP} {TURN}"


def validate(entry: str) -> None:
    """Enforce the competition gate: one line, 1-200 chars, UTF-8-safe."""
    if not 1 <= len(entry) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} chars, got {len(entry)}")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    entry.encode("utf-8")


def write_entry(entry: str) -> Path:
    """Write the entry, then read it back and confirm byte equality."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(entry, encoding="utf-8")
    round_tripped = OUTPUT_PATH.read_text(encoding="utf-8")
    if round_tripped != entry:
        raise RuntimeError("round-trip mismatch: file content differs from entry")
    return OUTPUT_PATH


def main() -> int:
    entry = build_entry()
    if entry != EXPECTED:
        raise RuntimeError("built entry does not match the chosen line")
    validate(entry)
    path = write_entry(entry)
    print(f"wrote {len(entry)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
