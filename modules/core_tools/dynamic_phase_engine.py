# Dynamic Phase Progression/Regression Engine


def should_progress(user, compliance_trend, feedback):
    """Decide if the user should advance a phase."""
    # Example: high compliance, low pain/fatigue, high mood, session quality trending up
    return (
        compliance_trend > 0.85 and
        feedback.pain < 4 and
        feedback.fatigue < 4 and
        feedback.mood > 6
    )


def should_regress(user, compliance_trend, feedback):
    """Decide if the user should regress a phase."""
    # Example: poor compliance, high pain/fatigue, low mood, frequent overrides
    return (
        compliance_trend < 0.65 or
        feedback.pain > 7 or
        feedback.fatigue > 7 or
        feedback.mood < 3
    )
