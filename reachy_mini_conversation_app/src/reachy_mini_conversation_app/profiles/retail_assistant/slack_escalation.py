"""Slack escalation tool for Reachy Mini Retail Assistant."""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from reachy_mini_conversation_app.tools.core_tools import Tool, ToolDependencies


logger = logging.getLogger(__name__)
DATA_DIR = Path(os.getenv("REACHY_MINI_DATA_DIR", "data"))


class SlackEscalationTool(Tool):
    """Escalate high-value signals to the organization via Slack."""

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
                ),
            },
            "summary": {
                "type": "string",
                "description": "Concise summary of the situation (1-2 sentences)",
            },
            "evidence": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of specific observations that led to this escalation",
            },
            "recommendation": {
                "type": "string",
                "description": "Optional: Suggested next action for the team",
            },
        },
        "required": ["signal_type", "summary", "evidence"],
    }

    def _webhook(self) -> Optional[str]:
        return os.getenv("SLACK_WEBHOOK_URL")

    def _app_meta(self) -> str:
        app_name = os.getenv("REACHY_MINI_APP_NAME", "reachy_mini_conversation_app")
        app_version = os.getenv("REACHY_MINI_APP_VERSION", "dev")
        return f"{app_name} v{app_version}"

    def _format_slack_message(
        self,
        signal_type: str,
        summary: str,
        evidence: List[str],
        recommendation: Optional[str] = None,
    ) -> Dict[str, Any]:
        emoji_map = {
            "demand": "📦",
            "confusion": "❓",
            "risk": "⚠️",
            "memory": "🧠",
        }
        emoji = emoji_map.get(signal_type, "🤖")

        blocks: List[Dict[str, Any]] = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"{emoji} Reachy Escalation: {signal_type.title()}"},
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Summary:*\n{summary}"},
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*Evidence:*\n" + "\n".join(f"• {e}" for e in evidence)},
            },
        ]

        if recommendation:
            blocks.append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*Recommendation:*\n{recommendation}"},
                }
            )

        blocks.append(
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"Escalated by Reachy Mini • {self._app_meta()}"}
                ],
            }
        )

        return {"blocks": blocks}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    async def _send_to_slack(self, payload: Dict[str, Any]) -> None:
        webhook = self._webhook()
        if not webhook:
            raise ValueError("SLACK_WEBHOOK_URL not configured")

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(webhook, json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()

    async def __call__(
        self,
        deps: ToolDependencies,
        signal_type: str,
        summary: str,
        evidence: List[str],
        recommendation: Optional[str] = None,
        **_: Any,
    ) -> Dict[str, Any]:
        logger.info("Escalating %s signal to Slack: %s", signal_type, summary)

        if not evidence:
            return {"success": False, "message": "Evidence is required for escalation"}

        webhook = self._webhook()
        payload = self._format_slack_message(signal_type, summary, evidence, recommendation)

        if not webhook:
            # Fallback: log to disk so we never lose the escalation
            fallback_file = DATA_DIR / "escalations.json"
            fallback_file.parent.mkdir(parents=True, exist_ok=True)
            existing: List[Dict[str, Any]] = []
            if fallback_file.exists():
                try:
                    with open(fallback_file, "r", encoding="utf-8") as f:
                        existing = json.load(f)
                except Exception:
                    existing = []

            existing.append(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "signal_type": signal_type,
                    "summary": summary,
                    "evidence": evidence,
                    "recommendation": recommendation,
                    "status": "not_sent_slack_unavailable",
                }
            )

            with open(fallback_file, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2)

            logger.warning("Slack webhook not configured; escalation logged to %s", fallback_file)
            return {
                "success": True,
                "message": "Escalation logged locally (Slack not configured). Set SLACK_WEBHOOK_URL to send to Slack.",
                "signal_type": signal_type,
                "fallback": "local_logging",
            }

        try:
            await self._send_to_slack(payload)
            logger.info("Successfully escalated %s signal to Slack", signal_type)
            return {
                "success": True,
                "message": f"Successfully notified team about {signal_type} signal",
                "signal_type": signal_type,
            }
        except httpx.HTTPError as exc:
            logger.error("Failed to send Slack message: %s", exc, exc_info=True)
            return {"success": False, "message": f"Failed to send Slack message: {exc}"}
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Unexpected error during escalation: %s", exc, exc_info=True)
            return {"success": False, "message": f"Unexpected error: {exc}"}

__all__ = ["SlackEscalationTool"]
