import difflib
from .repo_manager import RepoManager


class ChangeApplier:
    """Apply either full-file replacements or unified-diff patches."""

    def __init__(self, repo: RepoManager):
        self.repo = repo

    # direct replacement
    def apply_full(self, rel: str, new_text: str):
        self.repo.write(rel, new_text)

    # unified diff patch (expects standard unified-diff format)
    def apply_patch(self, rel: str, patch: str):
        old_lines = self.repo.read(rel).splitlines(keepends=True)
        diff_lines = patch.splitlines(keepends=True)

        new_lines: list[str] = []
        i = 0
        for line in diff_lines:
            if line.startswith(("---", "+++", "@@")):
                continue
            if line.startswith(" "):
                new_lines.append(old_lines[i])
                i += 1
            elif line.startswith("-"):
                i += 1
            elif line.startswith("+"):
                new_lines.append(line[1:])
        if i < len(old_lines):
            new_lines.extend(old_lines[i:])
        self.repo.write(rel, "".join(new_lines))
