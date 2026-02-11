"""Slack escalation tool for Reachy Mini Retail Assistant.

This tool allows Reachy to escalate high-value signals to the organization
via Slack webhooks. It follows the conversation app's Tool base class pattern.
"""

import json
import logging
from typing import Any, Dict

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from reachy_mini_karen_whisperer import settings

# Import Tool base class from conversation app
try:
    from reachy_mini_karen_whisperer.tools.core_tools import Tool, ToolDependencies
except ImportError:
    # Fallback if conversation app not installed
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


class SlackEscalationTool(Tool):
    """Escalate high-value signals to organization via Slack.
    
    This tool represents an explicit decision by Reachy to notify the team
    about patterns or situations that warrant human attention.
    
    Design principles:
    - Agency over automation (Reachy decides when)
    - Judgment over logging (not every interaction)
    - Restraint over noise (escalate rarely but meaningfully)
    - Explainability (provide evidence and reasoning)
    """
    
    name = "escalate_to_slack"
    description = (
        "Notify the organization of a high-value signal that warrants human attention. "
        "Use this when you detect patterns like: repeated product requests you can't fulfill, "
        "confusion about the same topic multiple times, or risk situations (frustration, safety concerns). "
        "Always provide clear evidence and a recommendation."
    )
    
    parameters_schema = {
        "type": "object",
        "properties": {
            "signal_type": {
                "type": "string",
                "enum": ["demand", "confusion", "risk", "memory"],
                "description": (
                    "Type of signal: "
                    "demand = many requests for unavailable items, "
                    "confusion = repeated questions despite answers, "
                    "risk = frustration/safety/uncertainty spike, "
                    "memory = long-term insight worth preserving"
                )
            },
            "summary": {
                "type": "string",
                "description": "Concise summary of the situation (1-2 sentences)"
            },
            "evidence": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of specific observations that led to this escalation"
            },
            "recommendation": {
                "type": "string",
                "description": "Optional: Suggested next action for the team"
            }
        },
        "required": ["signal_type", "summary", "evidence"]
    }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def _send_to_slack(self, payload: Dict[str, Any]) -> None:
        """Send payload to Slack with retry logic."""
        if not settings.slack_webhook_url:
            raise ValueError("SLACK_WEBHOOK_URL not configured")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                settings.slack_webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
    
    def _format_slack_message(
        self,
        signal_type: str,
        summary: str,
        evidence: list[str],
        recommendation: str = None
    ) -> Dict[str, Any]:
        """Format message for Slack with rich formatting."""
        # Signal type emoji mapping
        emoji_map = {
            "demand": "📦",
            "confusion": "❓",
            "risk": "⚠️",
            "memory": "🧠"
        }
        
        emoji = emoji_map.get(signal_type, "🤖")
        
        # Build blocks for rich Slack message
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} Reachy Escalation: {signal_type.title()}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Summary:*\n{summary}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Evidence:*\n" + "\n".join(f"• {e}" for e in evidence)
                }
            }
        ]
        
        if recommendation:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Recommendation:*\n{recommendation}"
                }
            })
        
        blocks.append({
            "type": "context",
            "elements": [{
                "type": "mrkdwn",
                "text": f"Escalated by Reachy Mini • {settings.app_name} v{settings.app_version}"
            }]
        })
        
        return {"blocks": blocks}
    
    async def __call__(
        self,
        deps: ToolDependencies,
        signal_type: str,
        summary: str,
        evidence: list[str],
        recommendation: str = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Execute Slack escalation.
        
        Args:
            deps: Tool dependencies from conversation app
            signal_type: Type of signal (demand, confusion, risk, memory)
            summary: Brief summary of the situation
            evidence: List of specific observations
            recommendation: Optional suggested action
            
        Returns:
            Dict with success status and message
        """
        logger.info(
            f"Escalating {signal_type} signal to Slack: {summary}"
        )
        
        # Validate inputs
        if not evidence or len(evidence) == 0:
            return {
                "success": False,
                "message": "Evidence is required for escalation"
            }
        
        # Check if Slack is configured
        if not settings.slack_webhook_url:
            logger.warning("Slack webhook not configured - logging escalation locally")
            
            # Fallback: log to file
            from pathlib import Path
            import json
            from datetime import datetime
            
            escalation_file = Path("data/escalations.json")
            escalation_file.parent.mkdir(parents=True, exist_ok=True)
            
            escalation = {
                "timestamp": datetime.utcnow().isoformat(),
                "signal_type": signal_type,
                "summary": summary,
                "evidence": evidence,
                "recommendation": recommendation,
                "status": "not_sent_slack_unavailable"
            }
            
            # Load existing, append, save
            escalations = []
            if escalation_file.exists():
                try:
                    with open(escalation_file, 'r') as f:
                        escalations = json.load(f)
                except Exception:
                    pass
            
            escalations.append(escalation)
            
            with open(escalation_file, 'w') as f:
                json.dump(escalations, f, indent=2)
            
            return {
                "success": True,
                "message": f"Escalation logged locally (Slack not configured). Check data/escalations.json",
                "signal_type": signal_type,
                "fallback": "local_logging"
            }
        
        try:
            # Format and send message
            payload = self._format_slack_message(
                signal_type=signal_type,
                summary=summary,
                evidence=evidence,
                recommendation=recommendation
            )
            
            await self._send_to_slack(payload)
            
            logger.info(f"Successfully escalated {signal_type} signal to Slack")
            
            return {
                "success": True,
                "message": f"Successfully notified team about {signal_type} signal",
                "signal_type": signal_type
            }
            
        except httpx.HTTPError as e:
            logger.error(f"Failed to send Slack message: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Failed to send Slack message: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error during escalation: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}"
            }
