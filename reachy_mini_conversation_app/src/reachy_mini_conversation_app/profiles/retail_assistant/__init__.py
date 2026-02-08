"""Custom tools for Reachy Mini Retail Assistant."""

# Tools are loaded lazily to avoid conversation app dependency at import time
# They will be discovered by the conversation app's tool registry when needed

__all__ = [
    "SlackEscalationTool",
    "RecordInteractionSignalTool", 
    "CheckSignalAggregatesTool",
]


def __getattr__(name):
    """Lazy import tools to defer conversation app dependency."""
    if name == "SlackEscalationTool":
        from reachy_mini_retail_assistant.tools.slack_escalation import SlackEscalationTool
        return SlackEscalationTool
    elif name == "RecordInteractionSignalTool":
        from reachy_mini_retail_assistant.tools.signal_tracker import RecordInteractionSignalTool
        return RecordInteractionSignalTool
    elif name == "CheckSignalAggregatesTool":
        from reachy_mini_retail_assistant.tools.signal_aggregates import CheckSignalAggregatesTool
        return CheckSignalAggregatesTool
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
