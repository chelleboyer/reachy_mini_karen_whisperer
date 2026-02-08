"""Signal aggregation tool - provides factual context about patterns."""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

from reachy_mini_conversation_app.tools.core_tools import Tool, ToolDependencies
from reachy_mini_conversation_app.profiles.retail_assistant.signal_tracker import _load_signals


logger = logging.getLogger(__name__)


class CheckSignalAggregatesTool(Tool):
    """Check aggregated signals for a specific entity/topic."""

    name = "check_signal_aggregates"
    description = (
        "Check aggregated signals for a specific topic or entity over a time window. "
        "Use this when you suspect a pattern (e.g., multiple people asking about the same thing). "
        "Returns counts and statistics to help you decide if escalation is needed."
    )

    parameters_schema = {
        "type": "object",
        "properties": {
            "entity": {
                "type": "string",
                "description": "The entity/topic to check (e.g., product name, location, topic)",
            },
            "window_hours": {
                "type": "number",
                "description": "How many hours back to check (e.g., 24 for last day)",
                "default": 24,
            },
        },
        "required": ["entity"],
    }

    async def __call__(
        self,
        deps: ToolDependencies,
        entity: str,
        window_hours: float = 24.0,
        **_: Any,
    ) -> Dict[str, Any]:
        cutoff_time = datetime.utcnow() - timedelta(hours=window_hours)

        all_signals: List[Dict[str, Any]] = _load_signals()
        relevant_signals = [
            s
            for s in all_signals
            if s.get("entity", "").lower() == entity.lower()
            and datetime.fromisoformat(s.get("timestamp", "1970-01-01")) >= cutoff_time
        ]

        if not relevant_signals:
            return {
                "entity": entity,
                "window_hours": window_hours,
                "count": 0,
                "message": f"No signals found for '{entity}' in the last {window_hours} hours",
            }

        total_count = len(relevant_signals)
        unresolved_count = sum(1 for s in relevant_signals if not s.get("resolved", False))
        negative_sentiment_count = sum(
            1 for s in relevant_signals if s.get("sentiment") in ["frustrated", "angry"]
        )
        avg_confidence = sum(s.get("confidence", 0.0) for s in relevant_signals) / total_count

        results = {
            "entity": entity,
            "window_hours": window_hours,
            "count": total_count,
            "unresolved_count": unresolved_count,
            "unresolved_ratio": unresolved_count / total_count if total_count else 0,
            "negative_sentiment_count": negative_sentiment_count,
            "negative_sentiment_ratio": negative_sentiment_count / total_count if total_count else 0,
            "average_confidence": round(avg_confidence, 2),
            "recent_signals": [
                {
                    "intent": s.get("intent"),
                    "resolved": s.get("resolved"),
                    "sentiment": s.get("sentiment"),
                    "confidence": s.get("confidence"),
                }
                for s in relevant_signals[-5:]
            ],
        }

        logger.info(
            "Aggregate check for '%s': %s signals, %s unresolved, %s negative",
            entity,
            total_count,
            unresolved_count,
            negative_sentiment_count,
        )

        return results

__all__ = ["CheckSignalAggregatesTool"]
