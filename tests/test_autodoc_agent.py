from self_evolving_gpt.agents.autodoc_agent import AutoDocAgent
import tempfile, shutil, os


def test_autodoc_generates_files(tmp_path, monkeypatch):
    # copy a tiny module into temp repo
    pkg = tmp_path / "self_evolving_gpt"
    pkg.mkdir()
    mod = pkg / "__init__.py"
    mod.write_text("def foo(x):\n    \"\"\"echo\"\"\"\n    return x\n")
    (pkg / "agents").mkdir()
    monkeypatch.syspath_prepend(tmp_path)
    agent = AutoDocAgent(tmp_path)
    out = agent.run("generate docs", "")
    assert "Generated" in out
    api_dir = tmp_path / "docs" / "api"
    assert any(api_dir.iterdir())
