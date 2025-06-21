# \ud83d\udd10 Codex Block: SPEC004BATCH03CODEX_UTILITIES

Date: 2025-06-21

import os
import re
import hashlib
from datetime import datetime

CODEX_BLOCK_PATTERN = re.compile(r"^# \ud83d\udd10 Codex Block: SPEC(\d{3})BATCH(\d{2})([A-Z0-9_]+)")


def find_codex_blocks(base_dir: str = "."):
    """Scan repository and return Codex block metadata."""
    blocks = []
    for root, _, files in os.walk(base_dir):
        for fname in files:
            if fname.endswith(".py") or fname.endswith(".md"):
                path = os.path.join(root, fname)
                with open(path, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f):
                        match = CODEX_BLOCK_PATTERN.match(line)
                        if match:
                            blocks.append({
                                "spec_id": match.group(1),
                                "batch": match.group(2),
                                "block_id": match.group(3),
                                "file": path,
                                "line": i + 1,
                            })
    return blocks


def validate_codex_structure() -> bool:
    """Check for duplicate Codex blocks across the repo."""
    print("\n\ud83e\uddea Validating Codex Structure...")
    blocks = find_codex_blocks()
    seen = set()
    errors = 0
    for b in blocks:
        key = (b["spec_id"], b["batch"], b["block_id"])
        if key in seen:
            print(
                f"\u274c Duplicate Codex Block: SPEC{key[0]}BATCH{key[1]}{key[2]} "
                f"in {b['file']}:{b['line']}"
            )
            errors += 1
        seen.add(key)
    print(f"\u2705 Found {len(blocks)} valid codex blocks with {errors} issues.")
    return errors == 0


if __name__ == "__main__":
    validate_codex_structure()
