"""Signal tracking tool - records interaction signals for pattern detection."""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from reachy_mini_conversation_app.tools.core_tools import Tool, ToolDependencies


logger = logging.getLogger(__name__)

DATA_DIR = Path(os.getenv("REACHY_MINI_DATA_DIR", "data"))
SIGNAL_FILE = DATA_DIR / "signals.json"


def _load_signals() -> List[Dict[str, Any]]:
    """Load signals from JSON file."""
    if not SIGNAL_FILE.exists():
        return []
    try:
        with open(SIGNAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to load signals: %s", exc)
        return []


def _save_signals(signals: List[Dict[str, Any]]) -> None:
    """Persist signals to JSON file."""
    try:
        SIGNAL_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SIGNAL_FILE, "w", encoding="utf-8") as f:
            json.dump(signals, f, indent=2)
        logger.debug("Saved %s signals to %s", len(signals), SIGNAL_FILE)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to save signals: %s", exc)


class RecordInteractionSignalTool(Tool):
    """Record a summarized interaction signal for pattern detection."""

    name = "record_interaction_signal"
    description = (
        "Record a compact summary of a meaningful interaction. "
        "Call this after each substantive user interaction to track patterns over time. "
        "This helps detect if multiple people have similar issues or requests."
    )

    parameters_schema = {
        "type": "object",
        "properties": {
            "intent": {
                "type": "string",
                "description": "High-level user intent (e.g., product_search, directions, complaint, question)",
            },
            "entity": {
                "type": "string",
                "description": "Primary subject of interaction (e.g., specific product, location, topic)",
            },
            "resolved": {
                "type": "boolean",
                "description": "Whether you fully resolved the user's request",
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
                "description": "Your confidence in the response quality (0.0 to 1.0)",
            },
            "sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "frustrated", "angry"],
                "description": "User's sentiment during interaction",
            },
        },
        "required": ["intent", "entity", "resolved", "confidence", "sentiment"],
    }

    async def __call__(
        self,
        deps: ToolDependencies,
        intent: str,
        entity: str,
        resolved: bool,
        confidence: float,
        sentiment: str,
        **_: Any,
    ) -> Dict[str, Any]:
        signal = {
            "timestamp": datetime.utcnow().isoformat(),
            "intent": intent,
            "entity": entity,
            "resolved": resolved,
            "confidence": confidence,
            "sentiment": sentiment,
        }

        signals = _load_signals()
        signals.append(signal)
        _save_signals(signals)

        logger.debug(
            "Recorded signal: %s for '%s' (resolved=%s, confidence=%.2f, sentiment=%s)",
            intent,
            entity,
            resolved,
            confidence,
            sentiment,
        )

        return {
            "success": True,
            "message": "Signal recorded",
            "signal_count": len(signals),
        }

__all__ = ["RecordInteractionSignalTool"]
