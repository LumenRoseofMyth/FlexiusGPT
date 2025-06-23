from pydantic import BaseModel
import importlib


class Input(BaseModel):
    action: str
    data: dict = {}


DISPATCH_MAP = {
    "repo_audit": "modules.00_integrity_audit.interface",
    "repo_summary": "modules.module10_repo_analyzer.module10_repo_analyzer",
    "deep_summary": "modules.module15_deep_repo_orchestrator.interface",
    "meta_report": "modules.module16_meta_reporter.interface",
}


def run_module(*, payload: dict) -> dict:
    validated = Input(**payload)
    action = validated.action

    if action not in DISPATCH_MAP:
        return {
            "status": "error",
            "message": f"Unknown action: {action}",
        }

    module_path = DISPATCH_MAP[action]
    mod = importlib.import_module(module_path)

    if not hasattr(mod, "run_module"):
        return {
            "status": "error",
            "message": "Target module missing run_module",
        }

    result = mod.run_module(
        payload={"action": action, "data": validated.data}
    )

    return {
        "status": "ok",
        "source": action,
        "result": result,
    }
