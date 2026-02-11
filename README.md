---
title: Reachy Mini Karen Whisperer
emoji: 🛒
colorFrom: green
colorTo: blue
sdk: static
pinned: false
short_description: Diplomatic retail assistant with signal intelligence
tags:
 - reachy_mini
 - reachy_mini_python_app
---

# Reachy Mini Karen Whisperer

A diplomatic retail assistant that helps Reachy Mini handle difficult customer interactions with empathy and intelligence.

## Overview

The Karen Whisperer transforms Reachy Mini into a frontline retail agent capable of:
- **Empathetic Conversation**: Diplomatic responses using LLM-powered dialogue
- **Signal Intelligence**: Tracks interaction patterns to detect trends
- **Smart Escalation**: Automatically notifies teams via Slack when patterns warrant attention
- **Calming Gestures**: Uses expressive movements to create a soothing customer experience

## Features

### Signal Tracking
Records structured summaries of each interaction (intent, entity, resolution status, confidence, sentiment) to detect patterns over time.

### Aggregate Analysis
Checks accumulated signals to identify:
- High-demand products not in stock
- Repeated confusion about the same topics
- Frustration spikes or declining confidence

### Slack Escalation
When patterns cross thresholds, Reachy autonomously notifies the team with:
- Signal type (demand, confusion, risk, memory)
- Clear evidence
- Actionable recommendations

### Calming Behaviors
- Gentle head movements and soothing gestures
- Patient, understanding voice responses
- Active listening poses

## Installation

### Prerequisites

```bash
# Create virtual environment
cd reachy_mini_karen_whisperer
uv venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# source .venv/bin/activate    # Linux/macOS

# Install the app
uv pip install -e .
```

### Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Configure required settings in `.env`:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL_NAME=gpt-realtime
   SLACK_WEBHOOK_URL=your_slack_webhook_url  # Optional but recommended
   ```

3. (Optional) Set up Slack webhook:
   - Go to your Slack workspace settings
   - Create an incoming webhook
   - Add the URL to your `.env` file

## Usage

### Run the App

```bash
# Activate venv first
.\.venv\Scripts\Activate.ps1

# Run with Gradio interface (for simulation or remote testing)
reachy-mini-karen-whisperer --gradio

# Run in headless mode (when connected to physical robot)
reachy-mini-karen-whisperer
```

### Command Line Options

```bash
--gradio                 # Launch with Gradio web interface
--robot-name <name>      # Connect to specific robot
--debug                  # Enable debug logging
--no-camera              # Disable camera features
```

## How It Works

### 1. Interaction Recording
After each meaningful conversation, Reachy records a signal:
```python
{
  "intent": "product_search",
  "entity": "gluten-free bread",
  "resolved": false,
  "confidence": 0.7,
  "sentiment": "frustrated"
}
```

### 2. Pattern Detection
Reachy periodically checks aggregates:
- Are 25+ people asking about "gluten-free bread"?
- Are people repeatedly confused despite explanations?
- Is frustration spiking?

### 3. Autonomous Escalation
When thresholds are met, Reachy decides to notify the team via Slack with:
- Evidence of the pattern
- Statistics (count, resolution rate, sentiment)
- Recommended action

## Profile Configuration

The app is locked to the `karen_whisperer` profile in `src/reachy_mini_karen_whisperer/config.py`:

```python
LOCKED_PROFILE: str | None = "karen_whisperer"
```

Profile files are in `src/reachy_mini_karen_whisperer/profiles/karen_whisperer/`:
- `instructions.txt` - System prompt with diplomatic personality
- `tools.txt` - Enabled tools list

## Custom Tools

### Signal Tracker
```python
record_interaction_signal(
    intent="product_search",
    entity="gluten-free bread", 
    resolved=False,
    confidence=0.7,
    sentiment="frustrated"
)
```

### Signal Aggregates
```python
check_signal_aggregates(
    entity="gluten-free bread",
    window_hours=24
)
# Returns counts, resolution rates, sentiment analysis
```

### Slack Escalation
```python
escalate_to_slack(
    signal_type="demand",  # or confusion, risk, memory
    summary="High demand for gluten-free bread",
    evidence=["25 requests in 24hrs", "0% resolution rate"],
    recommendation="Stock gluten-free bread options"
)
```

## Development

### Project Structure

```
reachy_mini_karen_whisperer/
├── src/
│   └── reachy_mini_karen_whisperer/
│       ├── profiles/
│       │   └── karen_whisperer/
│       │       ├── instructions.txt      # System prompt
│       │       ├── tools.txt            # Tool configuration
│       │       ├── signal_tracker.py    # Profile-local copy
│       │       ├── signal_aggregates.py
│       │       └── slack_escalation.py
│       ├── tools/
│       │   ├── signal_tracker.py        # Main tool implementations
│       │   ├── signal_aggregates.py
│       │   ├── slack_escalation.py
│       │   └── ... (core conversation tools)
│       ├── config.py
│       ├── settings.py
│       └── main.py
├── data/                    # Created at runtime
│   ├── signals.json        # Interaction signals
│   └── escalations.json    # Escalation history (fallback)
├── .env
└── pyproject.toml
```

### Testing Without Slack

If `SLACK_WEBHOOK_URL` is not configured, escalations are saved to `data/escalations.json` instead.

### Customizing Thresholds

Edit `profiles/karen_whisperer/instructions.txt` to adjust escalation guidelines:
```
- **Demand**: ~25 unresolved requests in 24 hours
- **Confusion**: ~15 requests with 50%+ unresolved  
- **Risk**: 40%+ negative sentiment OR confidence <0.6
```

## Troubleshooting

### App won't start
- Check `.env` file has `OPENAI_API_KEY`
- Verify virtual environment is activated
- Check daemon is running: `reachy-mini-daemon status`

### Slack escalations not working
- Verify `SLACK_WEBHOOK_URL` in `.env`
- Test webhook manually with curl
- Check `data/escalations.json` for fallback logs

### No signals being recorded
- Check logs for tool execution
- Verify profile tools.txt includes signal_tracker
- Ensure LLM is calling the recording tool

## License

MIT License - see LICENSE file

## Contributing

Contributions welcome! Please open an issue or PR.

## Credits

Based on the [Reachy Mini Conversation App](https://github.com/pollen-robotics/reachy_mini_conversation_app) by Pollen Robotics.
