# Codex Upgrade Timestamp: 2025-06-20T04:09:43.837231Z
"""Feedback Engine module (module_id: 08_feedback_engine)"""

import logging
from datetime import datetime
import statistics

from modules.core_tools.feedback_types import MultiModalFeedback
from modules.core.twin.digital_twin_engine import DigitalTwin

MODULE_ID = "08_feedback_engine"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_module_use(module_id: str, action: str, result: str) -> None:
    """Log module usage in a structured format."""
    logger.info("module=%s action=%s result=%s", module_id, action, result)


digital_twin = None


def init_digital_twin(user_profile: dict) -> None:
    """Initialize the digital twin for a user profile."""
    global digital_twin
    digital_twin = DigitalTwin(user_profile)


def process_feedback(user_profile: dict, feedback_data: dict, session_outcome=None, context=None) -> str:
    """Update digital twin with feedback and return suggested nudge."""
    global digital_twin
    if digital_twin is None:
        init_digital_twin(user_profile)
    feedback = MultiModalFeedback(**feedback_data)
    digital_twin.update(feedback, session_outcome, context or {})
    log_module_use(MODULE_ID, "process_feedback", "updated")
    return digital_twin.suggest_nudge()


module_map = {
    "process_feedback": process_feedback,
    "init_digital_twin": init_digital_twin,
}


def _commit_sentiment(messages: list[str]) -> str:
    """Very naive sentiment check on commit messages."""
    pos = ["add", "improve", "fix", "refactor", "update"]
    neg = ["revert", "bug", "fail", "issue", "broken"]
    score = 0
    for msg in messages:
        low = msg.lower()
        if any(w in low for w in pos):
            score += 1
        if any(w in low for w in neg):
            score -= 1
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"

def generate_coding_feedback(daily_metrics: list) -> list:
    """Generate coding-specific feedback from daily metrics."""
    feedback = []
    twin = {}
    if digital_twin is not None:
        twin = digital_twin.state.get("meta", {})
    for metric in daily_metrics:
        # START UPGRADE_BLOCK_CODING_FEEDBACK
        if metric["type"] == "coding":
            if metric["metrics"].get("pull_requests", 0) > 2:
                feedback.append("✅ Productive coding day! Keep reviewing your PRs.")
            else:
                feedback.append(
                    "👀 Try to review or push at least 2 PRs a day to build consistency."
                )
            # START UPGRADE_BLOCK_TREND_FEEDBACK
            week_delta = twin.get("coding_week_delta", 0)
            if week_delta > 1:
                feedback.append("📈 Your coding productivity increased 2x this week. Great trend!")
            elif week_delta < -1:
                feedback.append("⚠️ Your coding activity dropped. Let's explore what affected your flow.")
            else:
                feedback.append("🧭 Consistent effort—stay steady and focused this week.")
            # END
            # START UPGRADE_BLOCK_PEAK_PERFORMANCE_FEEDBACK
            lines_added = metric["metrics"].get("lines_added", 0)
            if lines_added > 1000:
                feedback.append(
                    "🚀 Massive code push detected! Don’t forget to review and refactor."
                )
            elif lines_added < 50:
                feedback.append(
                    "📉 Low commit volume—was this intentional? Consider a micro-task."
                )
            else:
                feedback.append(
                    "📊 Solid day—your commit size was balanced. Maintain quality."
                )
            # END
            # START UPGRADE_BLOCK_RECOVERY_FEEDBACK
            if metric["type"] == "coding" and twin.get("peak_push_flag"):
                feedback.append(
                    "🛑 You had a heavy push recently. Take a step back—review, refactor, or document your code today."
                )
            elif twin.get("coding_week_delta", 0) < 0:
                feedback.append(
                    "🔄 Regression detected. Now’s a good time for cleanup or learning sprints."
                )
            else:
                feedback.append(
                    "😌 Balanced phase—consider some light tasks or mentoring others."
                )
            # END
            # START CODE_ANALYTICS_SIMULATION_FEEDBACK
            msgs = metric.get("data", {}).get("commit_messages", [])
            if msgs:
                sentiment = _commit_sentiment(msgs)
                if sentiment == "positive":
                    feedback.append("✨ Positive commit energy detected.")
                elif sentiment == "negative":
                    feedback.append("😟 Commit tone negative—take a short break.")
                else:
                    feedback.append("💬 Commit tone neutral.")

            if digital_twin and digital_twin.simulate_fatigue_risk():
                feedback.append("⚠️ Simulation: potential mental fatigue risk.")
            # END
        # END
    return feedback

module_map.update({"generate_coding_feedback": generate_coding_feedback})
