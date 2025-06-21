import os, sys
sys.path.append(os.path.abspath("."))
from importlib import import_module
from pathlib import Path


def test_modules_have_run_module():
    base = Path('modules')
    for mod in base.iterdir():
        if not mod.is_dir():
            continue
        if '_' not in mod.name:
            continue
        target = mod / f"{mod.name.split('_',1)[1]}.py"
        if not target.exists():
            continue
        pkg = f"modules.{mod.name}.{mod.name.split('_',1)[1]}"
        logic = import_module(pkg)
        assert hasattr(logic, 'run_module')
