from self_evolving_gpt.repo_manager import RepoManager
from self_evolving_gpt.change_applier import ChangeApplier


def test_apply_patch(tmp_path):
    repo = RepoManager(tmp_path)
    ca = ChangeApplier(repo)
    rel = "x.py"
    repo.write(rel, "print('A')\n")
    patch = """\
--- a/x.py
+++ b/x.py
@@
-print('A')
+print('B')
"""
    ca.apply_patch(rel, patch)
    assert "B" in repo.read(rel)
