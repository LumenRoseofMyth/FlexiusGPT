from pathlib import Path
import hashlib


class RepoManager:
    """Read, write, list, and hash files in the repository root."""

    def __init__(self, root: str = "."):
        self.root = Path(root).resolve()

    # ───── basic I/O ─────
    def read(self, rel: str) -> str:
        return (self.root / rel).read_text(encoding="utf-8")

    def write(self, rel: str, text: str) -> None:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    # ───── helpers ─────
    def list_py(self) -> list[str]:
        return [
            str(p.relative_to(self.root))
            for p in self.root.rglob("*.py")
            if "__pycache__" not in p.parts
        ]

    def md5(self, rel: str) -> str:
        data = self.read(rel).encode()
        return hashlib.md5(data).hexdigest()
