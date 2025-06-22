from importlib import import_module
from fastapi import HTTPException

REGISTRY: dict[str, callable] = {}


def _lazy_import(module_id: str):
    if module_id in REGISTRY:
        return REGISTRY[module_id]
    pkg = f"modules.{module_id}.{module_id.split('_',1)[1]}"
    try:
        mod = import_module(pkg)
        REGISTRY[module_id] = mod.run_module
        return REGISTRY[module_id]
    except ModuleNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Module {module_id} missing") from e


def call_module_logic(module_id: str, payload: dict):
    fn = _lazy_import(module_id)
    return fn(payload=payload)


def run_workflow(name: str, payload: dict | None = None):
    from workflows import WORKFLOWS
    if name not in WORKFLOWS:
        print(f"Unknown workflow: {name}")
        return None
    payload = payload or {}
    return WORKFLOWS[name](payload=payload)
