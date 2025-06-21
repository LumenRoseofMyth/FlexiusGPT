from core.router.validator import validate_payload

WORKFLOWS = {}


def _register(name: str):
    def deco(fn):
        WORKFLOWS[name] = validate_payload(fn)
        return fn
    return deco

from .deep_dive_review import run as _deep_dive_review

@_register("deep_dive_review")
def deep_dive_review(*, user_log: dict | None = None) -> dict:
    _deep_dive_review(user_log)
    return {"success": True}
