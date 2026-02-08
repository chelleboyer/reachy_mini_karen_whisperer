"""
🤖 THE KAREN WHISPERER 🤖
Reachy Mini Retail Assistant - Landing Page for HF Spaces
"""
import gradio as gr

# Story content
TITLE = "🤖 The Karen Whisperer - Reachy Mini Retail Assistant"

DESCRIPTION = """
An AI-powered retail assistant that combines **emotional intelligence**, **pattern detection**, 
and **smart escalation** to handle challenging customer interactions with grace.

**Powered by:**
- OpenAI Realtime API for natural conversation
- Custom signal tracking & pattern detection
- Slack integration for intelligent escalation
- Reachy Mini's expressive movements
"""

STORY = """
## The Problem

Retail workers face challenging customer interactions daily. "Karen" moments—where frustrated 
customers need immediate attention—can overwhelm staff and impact store operations.

## The Solution

**The Karen Whisperer** is a Reachy Mini robot assistant that:

1. **Listens & Understands**: Natural voice conversation with emotional intelligence
2. **Tracks Patterns**: Records interaction signals (intent, sentiment, resolution status)
3. **Detects Trends**: Analyzes aggregated signals to identify recurring issues
4. **Smart Escalation**: Automatically alerts management via Slack when patterns emerge

## How It Works

### Signal Tracking
Every interaction is recorded with:
- Customer intent (product inquiry, complaint, etc.)
- Entity mentioned (product name, service)
- Resolution status (resolved, unresolved, escalated)
- Confidence level and sentiment

### Pattern Detection
Aggregates signals over time to identify:
- High-frequency product inquiries
- Recurring complaints or issues
- Unresolved interaction patterns
- Sentiment trends

### Intelligent Escalation
When thresholds are exceeded:
- Sends structured Slack notifications to management
- Includes actionable insights and signal summaries
- Enables proactive problem-solving

## Technical Stack

- **Voice AI**: OpenAI Realtime API with custom tools
- **Robot Platform**: Reachy Mini by Pollen Robotics
- **Signal Intelligence**: Custom Python tools for tracking & aggregation
- **Integration**: Slack webhooks for team notifications
- **UI**: Gradio interface with live transcripts

## Custom Tools

### `record_interaction_signal`
Logs customer interactions with structured data:
- Intent, entity, sentiment, confidence
- Resolution status and notes

### `get_signal_aggregates`
Analyzes patterns across interactions:
- Total signals, unique entities
- Frequency distributions
- Sentiment trends

### `escalate_to_slack`
Sends structured alerts to management:
- Pattern summaries
- Actionable insights
- Aggregate statistics

## Impact

- **Reduced staff burnout** - Robot handles front-line interactions
- **Proactive management** - Issues identified before escalation
- **Better customer experience** - Consistent, patient responses
- **Data-driven insights** - Pattern detection informs inventory & training

---

Built for the **Reachy Mini AI Competition** 🏆
"""

FEATURES = """
### Key Features

✨ **Natural Conversation** - Voice-based interaction with customers  
👁️ **Visual Awareness** - Camera perception for engagement  
💃 **Expressive Movements** - Head, body, and antenna animations  
📊 **Pattern Detection** - Tracks signals to identify trends  
🚨 **Smart Escalation** - Alerts management automatically  
😊 **Emotional Intelligence** - Responds to customer sentiment  
"""

# Build the Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="The Karen Whisperer") as demo:
    gr.Markdown(f"# {TITLE}")
    gr.Markdown(DESCRIPTION)
    
    with gr.Tabs():
        with gr.Tab("📖 Story"):
            gr.Markdown(STORY)
        
        with gr.Tab("✨ Features"):
            gr.Markdown(FEATURES)
            gr.Markdown("""
            ### Architecture
            
            ```
            Customer Interaction
                    ↓
            Reachy Mini (Voice + Vision)
                    ↓
            OpenAI Realtime API
                    ↓
            Signal Tracking Tools
                    ↓
            Pattern Detection Engine
                    ↓
            Slack Escalation (when needed)
            ```
            """)
        
        with gr.Tab("🔧 Technical Details"):
            gr.Markdown("""
            ### Custom Tools Implementation
            
            #### Signal Tracker
            Records each interaction with structured metadata stored in JSON.
            
            #### Aggregator
            Analyzes signal database to detect:
            - High-frequency entities (products, issues)
            - Sentiment trends
            - Resolution patterns
            
            #### Escalator
            Triggers Slack notifications when:
            - Signal count exceeds threshold
            - Sentiment drops below threshold
            - Specific critical issues detected
            
            ### Profile Configuration
            Uses custom retail_assistant profile with:
            - Specialized instructions for pattern detection
            - Custom tool definitions
            - Escalation logic
            
            ### Data Storage
            Signals stored in `data/signals.json` with schema:
            ```json
            {
              "timestamp": "ISO-8601",
              "intent": "product_inquiry|complaint|...",
              "entity": "product_name",
              "resolved": true|false,
              "confidence": 0.0-1.0,
              "sentiment": "positive|neutral|negative",
              "notes": "Additional context"
            }
            ```
            """)
        
        with gr.Tab("🎬 Demo"):
            gr.Markdown("""
            ## Live Demo
            
            ⚠️ **Note**: Full demo requires:
            - Reachy Mini robot hardware
            - OpenAI API key
            - Slack webhook URL
            
            This Space showcases the concept and architecture.
            
            ### Try It Locally
            
            Clone the repository and run:
            ```bash
            git clone https://github.com/chelleboyer/reachy_mini_karen_whisperer
            cd reachy_mini_karen_whisperer
            # Set environment variables
            export OPENAI_API_KEY=your_key
            export SLACK_WEBHOOK_URL=your_webhook
            # Run the app
            python -m reachy_mini_conversation_app --gradio --profile retail_assistant
            ```
            """)
    
    gr.Markdown("""
    ---
    
    ### Links
    
    - 🤖 [Reachy Mini by Pollen Robotics](https://www.pollen-robotics.com/reachy-mini/)
    - 📚 [Conversation App](https://github.com/pollen-robotics/reachy_mini_conversation_app)
    - 🏆 Built for Reachy Mini AI Competition
    
    **The Karen Whisperer** - Powered by AI. Trained in patience. Snack-motivated.
    """)

if __name__ == "__main__":
    demo.launch()
