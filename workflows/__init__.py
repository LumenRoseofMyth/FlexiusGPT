from core.router.validator import validate_payload

WORKFLOWS = {}


from typing import Callable, Dict, Any

def _register(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        WORKFLOWS[name] = validate_payload(fn)
        return fn
    return deco

from typing import Callable, Optional

from .deep_dive_review import run as _deep_dive_review

_deep_dive_review: Callable[[Optional[str]], None]

@_register("deep_dive_review")
def deep_dive_review(*, user_log: str | None = None) -> Dict[str, bool]:
    _deep_dive_review(user_log)
    return {"success": True}
