import json
import os
from datetime import datetime

LOG_PATH = os.path.join('logs', 'connector_audit_log.json')

def log_connector_call(module: str, action: str, status: str, output: str) -> dict:
    """Append a connector call record to the audit log."""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "module": module,
        "action": action,
        "status": status,
        "output": output,
    }
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    try:
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = []
    data.append(entry)
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return entry

if __name__ == '__main__':
    import sys
    module = sys.argv[1] if len(sys.argv) > 1 else 'deep_repo_orchestrator'
    action = sys.argv[2] if len(sys.argv) > 2 else 'repo_orchestrator'
    res = log_connector_call(module, action, 'success', 'ok')
    print(json.dumps(res, indent=2))
