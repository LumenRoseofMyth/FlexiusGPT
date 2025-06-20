from self_evolving_gpt.repo_manager import RepoManager
import hashlib


def test_read_write_md5_roundtrip(tmp_path):
    repo = RepoManager(tmp_path)
    rel = "sample.txt"
    content = "hello"
    repo.write(rel, content)
    assert repo.read(rel) == content
    assert repo.md5(rel) == hashlib.md5(content.encode()).hexdigest()
