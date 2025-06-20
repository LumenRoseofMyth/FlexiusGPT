import subprocess
import sys
from pathlib import Path


class TestRunner:
    """Runs pytest within the repo and captures output."""

    def __init__(self, repo_root: str = "."):
        self.root = Path(repo_root).resolve()

    def run(self) -> bool:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        (self.root / "test_output.log").write_text(result.stdout)
        return result.returncode == 0
