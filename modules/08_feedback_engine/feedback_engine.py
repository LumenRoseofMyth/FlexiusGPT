# Codex Upgrade Timestamp: 2025-06-20T04:09:43.837231Z
"""Feedback Engine module (module_id: 08_feedback_engine)"""

import logging

from modules.core_tools.feedback_types import MultiModalFeedback
from modules.core_tools.digital_twin_engine import DigitalTwin

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
