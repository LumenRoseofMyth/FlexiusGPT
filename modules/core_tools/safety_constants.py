# Dynamic guardrail registry for HIMKS

def get_guardrail(name, profile):
    GUARDRAILS = {
        'sleep': lambda p: p.get('sleep_baseline', 8) * 0.75,
        'hrv': lambda p: p.get('hrv_baseline', 70) * 0.85,
        # Add more as needed
    }
    if name in GUARDRAILS:
        return GUARDRAILS[name](profile)
    raise ValueError(f"Unknown guardrail: {name}")

