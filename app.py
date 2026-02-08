"""
The Karen Whisperer - Reachy Mini Retail Assistant
Landing Page for HF Spaces (matching marketing site design)
"""
import gradio as gr

# Custom CSS matching the marketing site
custom_css = """
.gradio-container {
    background-color: #f8f9fa;
}
.hero-section {
    padding: 2rem 1.5rem;
    margin-bottom: 2rem;
}
.hero-content {
    text-align: left;
    padding-right: 1.5rem;
}
.hero-title {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
    color: #000000;
}
.hero-subtitle {
    font-size: 1.3rem;
    margin-bottom: 1rem;
    color: #2c3e50;
}
.hero-description {
    font-size: 1rem;
    color: #34495e;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}
.stats-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.stat-box {
    background: white;
    padding: 1.25rem;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    border: 1px solid #e0e0e0;
    flex: 1;
    min-width: 150px;
}
.feature-card {
    padding: 1.5rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    margin-bottom: 1rem;
    background: white;
}
.step-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border-left: 4px solid #667eea;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}
"""

# Build the Gradio interface
with gr.Blocks(title="The Karen Whisperer") as demo:
    
    # Hero Section
    with gr.Row(elem_classes="hero-section"):
        with gr.Column(scale=1, elem_classes="hero-content"):
            gr.Markdown("# Meet Reachy Mini\n## Retail Assistant", elem_classes="hero-title")
            gr.Markdown("### Your tiny, charming Retail Assistant - aka the Karen Whisperer", elem_classes="hero-subtitle")
            gr.Markdown("**Small robot. Big patience.** De-escalation with built-in chill mode - he handles the \"Can I speak to your manager?\" so you don't have to.", elem_classes="hero-description")
            
            # Stats
            with gr.Row(elem_classes="stats-row"):
                with gr.Column(scale=1, elem_classes="stat-box"):
                    gr.Markdown("### 99%\nDe-escalation Rate")
                with gr.Column(scale=1, elem_classes="stat-box"):
                    gr.Markdown("### <2s\nResponse Time")
                with gr.Column(scale=1, elem_classes="stat-box"):
                    gr.Markdown("### 24/7\nAlways On")
        
        with gr.Column(scale=1):
            gr.HTML("""
            <div style="padding: 1rem;">
            <h3 style="color: #000000; margin-bottom: 0.75rem;">See It In Action</h3>
            <p><a href="https://thekarenwhisperer.lovable.app/" target="_blank" rel="noopener noreferrer" style="color: #0066cc; text-decoration: underline; font-weight: 600; font-size: 1.05rem;">Interactive Demo</a></p>
            <p style="color: #34495e; margin-top: 0.5rem; font-size: 0.95rem;">Experience the full Karen Whisperer concept with interactive <a href="https://thekarenwhisperer.lovable.app/" target="_blank" rel="noopener noreferrer" style="color: #0066cc; text-decoration: underline; font-weight: 600; font-size: 1.05rem;">storytelling</a>.</p>
            </div>
            """)
    
    # What Reachy Can Do
    gr.Markdown("## What Reachy Mini Can Do")
    gr.Markdown("Customer service superpowers, minus the cape. Here's how Reachy keeps his cool while keeping customers happy.")
    
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Group(elem_classes="feature-card"):
                gr.Markdown("### Smart Q&A")
                gr.Markdown("Answers common questions about returns, prices, store hours, and policies instantly - no human needed.")
        
        with gr.Column(scale=1):
            with gr.Group(elem_classes="feature-card"):
                gr.Markdown("### Aisle Navigation")
                gr.Markdown("Guides customers to the right product or aisle in seconds, reducing wait times and frustration.")
    
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Group(elem_classes="feature-card"):
                gr.Markdown("### Issue Detection")
                gr.Markdown("Spots out-of-stock items and inventory issues, flagging them instantly for your team.")
        
        with gr.Column(scale=1):
            with gr.Group(elem_classes="feature-card"):
                gr.Markdown("### De-escalation Pro")
                gr.Markdown("Calms tense situations with friendly, professional prompts designed to diffuse conflict.")
    
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Group(elem_classes="feature-card"):
                gr.Markdown("### Smooth Escalation")
                gr.Markdown("When it's actually time for a human, hands off gracefully - politely and drama-free.")
        
        with gr.Column(scale=1):
            with gr.Group(elem_classes="feature-card"):
                gr.Markdown("### Lightning Fast")
                gr.Markdown("Sub-2-second response times keep customers engaged and conversations flowing.")
    
    # How It Works
    gr.Markdown("## How It Works")
    gr.Markdown("From \"Can I speak to your manager?\" to \"Thank you so much!\" - in three simple steps.")
    
    with gr.Column(elem_classes="step-card"):
        gr.Markdown("### 01 - Customer Approaches")
        gr.Markdown("A customer asks a question, makes a request, or... starts getting spicy. Reachy Mini is ready.")
        gr.Code("""// Incoming customer query
const mood = detectMood(customer);
// mood: "slightly_annoyed" -> "chill_mode_activated" """, language="typescript")
    
    with gr.Column(elem_classes="step-card"):
        gr.Markdown("### 02 - Instant Analysis")
        gr.Markdown("Reachy processes the request in milliseconds, understanding intent, emotion, and urgency.")
        gr.Code("""// AI-powered understanding
const response = await reachy.analyze({
  query: customer.message,
  context: storeData,
  deEscalationMode: true
});""", language="typescript")
    
    with gr.Column(elem_classes="step-card"):
        gr.Markdown("### 03 - Perfect Response")
        gr.Markdown("Delivers a friendly, helpful answer - or gracefully escalates when a human touch is truly needed.")
        gr.Code("""// Smooth handling
if (response.needsHuman) {
  return escalateGracefully(manager);
}
return sendResponse(response.message); // ✨""", language="typescript")
    
    # Technical Details
    with gr.Accordion("Technical Architecture", open=False):
        gr.Markdown("""
        ### Tech Stack
        
        - **Voice AI**: OpenAI Realtime API with function calling
        - **Robot Platform**: Reachy Mini by Pollen Robotics
        - **Pattern Detection**: Custom signal tracking & aggregation
        - **Escalation**: Slack webhook integration
        - **UI**: Gradio interface with live transcripts
        
        ### Custom Tools
        
        **Signal Tracker** - Records customer interactions with structured metadata (intent, sentiment, resolution status)
        
        **Aggregator** - Analyzes patterns across interactions to identify trends and recurring issues
        
        **Escalator** - Triggers Slack notifications when thresholds are exceeded or critical patterns emerge
        
        ### Try It Locally
        
        ```bash
        git clone https://github.com/chelleboyer/reachy_mini_karen_whisperer
        cd reachy_mini_karen_whisperer
        export OPENAI_API_KEY=your_key
        export SLACK_WEBHOOK_URL=your_webhook
        python -m reachy_mini_conversation_app --gradio --profile retail_assistant
        ```
        """)
    
    # Footer
    gr.Markdown("""
    ---
    
    ### Reachy Mini
    
    **Customer service with built-in chill mode.**
    
    [GitHub](https://github.com/chelleboyer/reachy_mini_karen_whisperer) | 
    [Hugging Face](https://huggingface.co/spaces/chelleboyer/reachy_mini_karen_whisperer) | 
    Built for [Reachy Mini AI Competition](https://www.pollen-robotics.com/)
    
    Made with love for retail heroes.
    """)

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(), css=custom_css)
