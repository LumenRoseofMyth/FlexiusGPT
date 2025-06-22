"""Feedback engine core logic."""

def record_feedback(user_id: str, feedback: str) -> dict:
    return {"user_id": user_id, "feedback": feedback}
