"""Settings module for tools to import configuration."""

from reachy_mini_karen_whisperer.config import config


# Expose config values that tools need
slack_webhook_url = config.SLACK_WEBHOOK_URL
app_name = config.APP_NAME
app_version = config.APP_VERSION
