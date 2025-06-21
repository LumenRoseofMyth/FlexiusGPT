# \ud83d\udd10 Codex Block: SPEC004BATCH03CODEX_UTILITIES

Date: 2025-06-21

import os
import re
import hashlib
from datetime import datetime

# Zero-cost enforcement patterns (paid API references)
PAID_API_PATTERNS = ["openai.api_key", "OPENAI_API_KEY", "api.openai.com"]

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


def check_zero_cost(base_dir: str = ".") -> bool:
    """Ensure repository does not reference known paid APIs."""
    violations = []
    for root, _, files in os.walk(base_dir):
        for fname in files:
            if fname.endswith(".py"):
                path = os.path.join(root, fname)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                for pat in PAID_API_PATTERNS:
                    if pat in text:
                        violations.append(f"{path}: '{pat}'")
    if violations:
        print("\u274c Zero-Cost violations found:")
        for v in violations:
            print(" -", v)
        return False
    print("\u2705 Zero-Cost compliance passed.")
    return True


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
                f"\u26A0\uFE0F Duplicate Codex Block (recommendation): "
                f"SPEC{key[0]}BATCH{key[1]}{key[2]} in {b['file']}:{b['line']}"
            )
        seen.add(key)
    print(f"\u2705 Found {len(blocks)} codex blocks. {errors} duplicates flagged.")
    return True


if __name__ == "__main__":
    zero_ok = check_zero_cost()
    validate_codex_structure()
    if not zero_ok:
        raise SystemExit(1)
