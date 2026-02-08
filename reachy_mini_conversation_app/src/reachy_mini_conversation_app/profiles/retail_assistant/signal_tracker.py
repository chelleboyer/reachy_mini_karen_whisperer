"""Signal tracking tool - records interaction signals for pattern detection.

This tool allows Reachy to record summarized interaction signals that can be
aggregated over time to detect patterns worth escalating.
"""

import json
import logging
from typing import Any, Dict
from datetime import datetime
from pathlib import Path

# Import Tool base class
try:
    from reachy_mini_retail_assistant.tools.core_tools import Tool, ToolDependencies
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


# Storage configuration
SIGNAL_FILE = Path("data/signals.json")


def _load_signals() -> list[Dict[str, Any]]:
    """Load signals from JSON file."""
    if not SIGNAL_FILE.exists():
        return []
    try:
        with open(SIGNAL_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load signals: {e}")
        return []


def _save_signals(signals: list[Dict[str, Any]]) -> None:
    """Save signals to JSON file."""
    try:
        SIGNAL_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SIGNAL_FILE, 'w') as f:
            json.dump(signals, f, indent=2)
        logger.debug(f"Saved {len(signals)} signals to {SIGNAL_FILE}")
    except Exception as e:
        logger.error(f"Failed to save signals: {e}")


# Simple in-memory storage (persisted to JSON)
SIGNAL_STORE: list[Dict[str, Any]] = []


class RecordInteractionSignalTool(Tool):
    """Record a summarized interaction signal.
    
    Each meaningful interaction produces a compact, structured summary that
    can be analyzed for patterns. This is NOT logging - it's signal extraction.
    
    Design principle: Judgment over Logging
    - Store structured signals, not raw transcripts
    - Focus on meaningful patterns, not every word
    """
    
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
                "description": "High-level user intent (e.g., product_search, directions, complaint, question)"
            },
            "entity": {
                "type": "string",
                "description": "Primary subject of interaction (e.g., specific product, location, topic)"
            },
            "resolved": {
                "type": "boolean",
                "description": "Whether you fully resolved the user's request"
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
                "description": "Your confidence in the response quality (0.0 to 1.0)"
            },
            "sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "frustrated", "angry"],
                "description": "User's sentiment during interaction"
            }
        },
        "required": ["intent", "entity", "resolved", "confidence", "sentiment"]
    }
    
    async def __call__(
        self,
        deps: ToolDependencies,
        intent: str,
        entity: str,
        resolved: bool,
        confidence: float,
        sentiment: str,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Record an interaction signal.
        
        Args:
            deps: Tool dependencies
            intent: User's intent
            entity: Main subject
            resolved: Whether request was fulfilled
            confidence: Confidence score 0-1
            sentiment: User sentiment
            
        Returns:
            Confirmation of recording
        """
        signal = {
            "timestamp": datetime.utcnow().isoformat(),
            "intent": intent,
            "entity": entity,
            "resolved": resolved,
            "confidence": confidence,
            "sentiment": sentiment
        }
        
        # Load existing signals, append new one, save back
        signals = _load_signals()
        signals.append(signal)
        _save_signals(signals)
        
        # Also keep in memory for fast access
        global SIGNAL_STORE
        SIGNAL_STORE = signals
        
        logger.debug(
            f"Recorded signal: {intent} for '{entity}' "
            f"(resolved={resolved}, confidence={confidence:.2f}, sentiment={sentiment})"
        )
        
        return {
            "success": True,
            "message": "Signal recorded",
            "signal_count": len(signals)
        }
