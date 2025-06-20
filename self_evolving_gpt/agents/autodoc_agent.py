import inspect, textwrap, importlib
from pathlib import Path
from types import ModuleType
from self_evolving_gpt.agents import AgentBase

class AutoDocAgent(AgentBase):
    """
    Generates Markdown API reference by introspecting python modules.
    Writes docs to docs/api/<module>.md
    """

    def __init__(self, repo_root: str = "."):
        self.repo = Path(repo_root).resolve()
        self.docs_dir = self.repo / "docs" / "api"
        self.docs_dir.mkdir(parents=True, exist_ok=True)

    # ── AgentBase interface ──
    def run(self, task: str, context: str) -> str:
        # task: "generate docs"
        modules = self._discover_modules()
        for m in modules:
            md = self._module_to_markdown(m)
            out = self.docs_dir / f"{m.__name__.replace('.','_')}.md"
            out.write_text(md, encoding="utf-8")
        return f"Generated {len(modules)} API files in docs/api/"

    def needs(self):
        return ["task"]

    # ── helpers ──
    def _discover_modules(self) -> list[ModuleType]:
        """Import all top-level self_evolving_gpt.* sub-packages."""
        pk_root = self.repo / "self_evolving_gpt"
        modules = []
        for path in pk_root.rglob("*.py"):
            rel = path.relative_to(self.repo).with_suffix("")
            mod_name = ".".join(rel.parts)
            try:
                modules.append(importlib.import_module(mod_name))
            except Exception:
                pass  # skip faulty import
        return modules

    def _module_to_markdown(self, module: ModuleType) -> str:
        lines = [f"# `{module.__name__}`\n"]
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) or inspect.isclass(obj):
                sig = ""
                try:
                    sig = str(inspect.signature(obj))
                except (TypeError, ValueError):
                    pass
                doc = inspect.getdoc(obj) or "No docstring."
                lines.append(f"## `{name}{sig}`\n")
                lines.append(textwrap.dedent(doc))
                lines.append("\n---\n")
        return "\n".join(lines)
