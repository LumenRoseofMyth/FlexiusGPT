import json
import sys
from typing import Any, Dict, List

def simulate_feedback(payload: Dict[str, Any]) -> Dict[str, Any]:
    trace: List[Dict[str, Any]] = []

    # FEEDBACK_ENGINE step
    trace.append({
        "engine": "FEEDBACK_ENGINE",
        "action": "parse_feedback",
        "result": payload,
    })

    # SAFETY_OVERRIDES step
    flagged = payload.get("flagged", False)
    safety_result = "rejected" if flagged else "approved"
    trace.append({
        "engine": "SAFETY_OVERRIDES",
        "action": "safety_check",
        "result": safety_result,
    })

    # SESSION_ENGINE step
    if not flagged:
        trace.append({
            "engine": "SESSION_ENGINE",
            "action": "update_session",
            "result": "feedback stored",
        })

    final = "accepted" if not flagged else "rejected"
    return {"trace": trace, "final_decision": final}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        payload = json.loads(sys.argv[1])
    else:
        payload = json.load(sys.stdin)
    out = simulate_feedback(payload)
    print(json.dumps(out, indent=2))
