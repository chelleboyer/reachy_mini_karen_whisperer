"""HF Space launcher for Reachy Mini Retail Assistant — The Karen Whisperer."""

import os
import sys

from fastapi import FastAPI

from reachy_mini_conversation_app import main as conversation_main
from reachy_mini_conversation_app.utils import parse_args


def build_app() -> FastAPI:
    """Build the FastAPI app and mount the Gradio UI for HF Spaces."""
    os.environ.setdefault("HF_SPACE", "1")
    os.environ.setdefault("REACHY_MINI_CUSTOM_PROFILE", "retail_assistant")

    # Force gradio mode for the conversation app
    sys.argv = [sys.argv[0], "--gradio"] + sys.argv[1:]
    args, _ = parse_args()

    settings_app = FastAPI()

    # The conversation app will mount Gradio onto settings_app when provided.
    conversation_main.run(
        args=args,
        robot=None,
        app_stop_event=None,
        settings_app=settings_app,
        instance_path=None,
    )

    return settings_app


app = build_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7860)
