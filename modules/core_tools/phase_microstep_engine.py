def microstep_phase(user, phase, micro_state):
    # Microsteps can be "ramp-up", "hold", "taper", or "fusion"
    if micro_state == "ramp-up" and user['compliance_streak'] > 5:
        return "hold"
    elif micro_state == "hold" and user['fatigue'] > 7:
        return "taper"
    elif micro_state == "taper" and user['mood'] > 6 and user['compliance_trend'] > 0.9:
        return "fusion"
    return micro_state
