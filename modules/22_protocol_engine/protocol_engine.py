# Codex Upgrade Timestamp: 2025-06-21
"""Protocol Engine module (module_id: 22_protocol_engine)"""

import logging

MODULE_ID = "22_protocol_engine"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_module_use(module_id: str, action: str, result: str) -> None:
    """Log module usage in a structured format."""
    logger.info("module=%s action=%s result=%s", module_id, action, result)


def recommend_next_protocol(twin_state: dict) -> list:
    """Return protocol recommendations based on digital twin metrics."""
    protocol = []
    twin = twin_state.get("meta", {})
    # START UPGRADE_BLOCK_PROTOCOL_RECS
    if twin.get("coding_week_delta", 0) >= 2:
        protocol.append(
            "🔁 Next goal: tackle a more complex pull request or join a peer code review."
        )
    elif twin.get("coding_week_delta", 0) <= -2:
        protocol.append(
            "🔄 Consider a micro-goal: code 30 min/day or resolve a small issue daily."
        )
    else:
        protocol.append(
            "✅ Maintain your rhythm—focus on clean, high-quality commits this week."
        )
    # END
    # START UPGRADE_BLOCK_RECOVERY_PROTOCOL
    if twin.get("peak_push_flag"):
        protocol.append(
            "🧘 Switch to recovery mode: No new PRs—focus on review, cleanup, or writing tests."
        )
    elif twin.get("coding_week_delta", 0) < 0:
        protocol.append(
            "🔁 Rebuild rhythm: One small, complete PR or fix a low-risk bug."
        )
    else:
        protocol.append(
            "🎯 Light goal: Write one wiki entry or improve onboarding docs."
        )
    # END
    log_module_use(MODULE_ID, "recommend_next_protocol", "generated")
    return protocol


def protocol_push_alert(metric: dict) -> list:
    """Provide nudges based on weekly pull request volume."""
    protocol = []
    # START UPGRADE_BLOCK_PEAK_PROTOCOL
    pr_count = metric["metrics"].get("pull_requests", 0)
    if pr_count >= 5:
        protocol.append(
            "🏁 Peak protocol: You’re eligible for an advanced challenge. Try debugging someone else’s code."
        )
    elif pr_count <= 1:
        protocol.append(
            "🔄 Let’s maintain flow. Aim for at least 2 PRs this week to stay in rhythm."
        )
    else:
        protocol.append(
            "🎯 Mid-range achieved—focus on deeper code quality this sprint."
        )
    # END
    return protocol


module_map = {
    "recommend_next_protocol": recommend_next_protocol,
    "protocol_push_alert": protocol_push_alert,
}
