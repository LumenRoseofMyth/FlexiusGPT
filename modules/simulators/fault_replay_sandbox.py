import json
import sys
from typing import Any, Dict, List

def replay_faults(events: List[str]) -> Dict[str, Any]:
    report = {"events": [], "modules": []}
    triggered = set()

    for event in events:
        modules = []
        if "hrv" in event.lower():
            modules.extend(["RECOVERY_STACK", "PHASE_MANAGER"])
        if "recovery" in event.lower():
            modules.append("SESSION_ENGINE")
        if not modules:
            modules.append("UNKNOWN")
        triggered.update(modules)
        report["events"].append({"event": event, "fallback": modules})

    report["modules"] = sorted(triggered)
    return report

if __name__ == "__main__":
    if len(sys.argv) > 1:
        events = json.loads(sys.argv[1])
    else:
        events = json.load(sys.stdin)
    out = replay_faults(events)
    print(json.dumps(out, indent=2))
