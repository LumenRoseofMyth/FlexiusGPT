# Codex Upgrade Timestamp: 2025-06-21
"""Ingestion Engine module (module_id: 21_ingestion_engine)"""

import logging
from typing import List, Dict, Any

MODULE_ID = "21_ingestion_engine"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_module_use(module_id: str, action: str, result: str) -> None:
    """Log module usage in a structured format."""
    logger.info("module=%s action=%s result=%s", module_id, action, result)


def ingest(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Ingest raw entries and extract metrics."""
    metrics_list = []
    for entry in entries:
        metrics = {"type": entry.get("type"), "source": entry.get("source")}
        # START UPGRADE_BLOCK_GITHUB_INGEST
        if entry["type"] == "coding" and entry["source"] == "GitHub":
            metrics["pull_requests"] = len(entry["data"].get("prs", []))
            metrics["lines_added"] = sum(pr.get("lines_added", 0) for pr in entry["data"].get("prs", []))
            metrics["lines_deleted"] = sum(pr.get("lines_deleted", 0) for pr in entry["data"].get("prs", []))
        # END
        metrics_list.append(metrics)
    log_module_use(MODULE_ID, "ingest", "complete")
    return metrics_list


module_map = {"ingest": ingest}
