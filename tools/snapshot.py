import argparse
import datetime
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Save Codex snapshot")
    parser.add_argument("rating", type=int, help="Current rating score")
    args = parser.parse_args()

    commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    timestamp = datetime.datetime.now().isoformat()

    codex_state = ""
    log_path = Path("codex_upgrade_log.txt")
    if log_path.exists():
        codex_state = log_path.read_text()

    snapshot = {
        "timestamp": timestamp,
        "commit": commit,
        "rating": args.rating,
        "codex_state": codex_state.splitlines(),
    }

    out_dir = Path("snapshots")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"{timestamp.replace(':', '-')}.json"
    out_file.write_text(json.dumps(snapshot, indent=2))
    print(f"Snapshot saved to {out_file}")


if __name__ == "__main__":
    main()
