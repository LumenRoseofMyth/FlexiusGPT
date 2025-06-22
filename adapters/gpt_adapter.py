from importlib import import_module
from fastapi import HTTPException
from typing import Callable, Any

REGISTRY: dict[str, Callable[[dict[str, Any]], Any]] = {}


def _lazy_import(module_id: str) -> Callable[..., Any]:
    if module_id in REGISTRY:
        return REGISTRY[module_id]
    pkg = f"modules.{module_id}.{module_id.split('_',1)[1]}"
    try:
        mod = import_module(pkg)
        REGISTRY[module_id] = mod.run_module
        return REGISTRY[module_id]
    except ModuleNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Module {module_id} missing") from e


def call_module_logic(module_id: str, payload: dict[str, Any] | None) -> Any:
    """Invoke a module's run_module function with standardized payload handling."""
    fn = _lazy_import(module_id)
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload must be a dictionary")
    try:
        return fn(payload=payload)
    except HTTPException as e:
        if e.status_code == 422:
            expected = getattr(fn, "__payload_model__", None)
            schema: dict[str, Any] = expected.model_json_schema().get("properties", {}) if expected else {}
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "Invalid payload",
                    "expected_schema": schema,
                    "received_payload": payload,
                },
            ) from e
        raise


from typing import Any, Callable, cast

def run_workflow(name: str, payload: dict[str, Any] | None = None) -> Any:
    from workflows import WORKFLOWS
    workflows_dict = cast(dict[str, Callable[[dict[str, Any]], Any]], WORKFLOWS)
    if name not in workflows_dict:
        print(f"Unknown workflow: {name}")
        return None
    payload = payload or {}
    result: Any = workflows_dict[name](payload)
    return result