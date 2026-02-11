"""Signal aggregation tool - provides factual context about patterns.

This tool allows Reachy to check aggregated signals over a time window
to make informed decisions about whether escalation is warranted.
"""

import logging
from typing import Any, Dict
from datetime import datetime, timedelta

from reachy_mini_karen_whisperer.tools.signal_tracker import _load_signals

# Import Tool base class
try:
    from reachy_mini_karen_whisperer.tools.core_tools import Tool, ToolDependencies
except ImportError:
    from abc import ABC, abstractmethod
    
    class Tool(ABC):
        name: str
        description: str
        parameters_schema: Dict[str, Any]
        
        def spec(self) -> Dict[str, Any]:
            return {
                "type": "function",
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters_schema,
            }
        
        @abstractmethod
        async def __call__(self, deps: Any, **kwargs: Any) -> Dict[str, Any]:
            raise NotImplementedError
    
    ToolDependencies = Any


logger = logging.getLogger(__name__)


class CheckSignalAggregatesTool(Tool):
    """Check aggregated signals for a specific entity/topic.
    
    Provides factual, aggregated context to help the agent decide
    if a pattern warrants escalation. Does NOT trigger escalation itself.
    
    Design principle: This tool informs, the agent decides.
    """
    
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
                "description": "The entity/topic to check (e.g., product name, location, topic)"
            },
            "window_hours": {
                "type": "number",
                "description": "How many hours back to check (e.g., 24 for last day)",
                "default": 24
            }
        },
        "required": ["entity"]
    }
    
    async def __call__(
        self,
        deps: ToolDependencies,
        entity: str,
        window_hours: float = 24.0,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Check signal aggregates for an entity.
        
        Args:
            deps: Tool dependencies
            entity: Entity to check
            window_hours: Hours to look back
            
        Returns:
            Aggregated statistics
        """
        # Calculate time window
        cutoff_time = datetime.utcnow() - timedelta(hours=window_hours)
        
        # Load signals from file
        all_signals = _load_signals()
        
        # Filter signals for this entity within time window
        relevant_signals = [
            s for s in all_signals
            if s["entity"].lower() == entity.lower()
            and datetime.fromisoformat(s["timestamp"]) >= cutoff_time
        ]
        
        if not relevant_signals:
            return {
                "entity": entity,
                "window_hours": window_hours,
                "count": 0,
                "message": f"No signals found for '{entity}' in the last {window_hours} hours"
            }
        
        # Aggregate statistics
        total_count = len(relevant_signals)
        unresolved_count = sum(1 for s in relevant_signals if not s["resolved"])
        negative_sentiment_count = sum(
            1 for s in relevant_signals 
            if s["sentiment"] in ["frustrated", "angry"]
        )
        
        # Calculate average confidence
        avg_confidence = sum(s["confidence"] for s in relevant_signals) / total_count
        
        # Compile results
        results = {
            "entity": entity,
            "window_hours": window_hours,
            "count": total_count,
            "unresolved_count": unresolved_count,
            "unresolved_ratio": unresolved_count / total_count if total_count > 0 else 0,
            "negative_sentiment_count": negative_sentiment_count,
            "negative_sentiment_ratio": negative_sentiment_count / total_count if total_count > 0 else 0,
            "average_confidence": round(avg_confidence, 2),
            "recent_signals": [
                {
                    "intent": s["intent"],
                    "resolved": s["resolved"],
                    "sentiment": s["sentiment"],
                    "confidence": s["confidence"]
                }
                for s in relevant_signals[-5:]  # Last 5 signals
            ]
        }
        
        logger.info(
            f"Aggregate check for '{entity}': {total_count} signals, "
            f"{unresolved_count} unresolved, {negative_sentiment_count} negative"
        )
        
        return results
