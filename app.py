"""
The Karen Whisperer - Reachy Mini Retail Assistant
Landing Page for HF Spaces (matching marketing site design)
"""
import gradio as gr

# Custom CSS for modern, attractive design
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.gradio-container {
    background: linear-gradient(135deg, #0d9488 0%, #06b6d4 100%) !important;
    min-height: 100vh;
    padding: 2rem 1rem !important;
}

.main-content {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    padding: 3rem 2.5rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

/* Typography */
.gradio-container h1, .gradio-container h2, .gradio-container h3, 
.gradio-container h4, .gradio-container h5, .gradio-container h6 {
    color: #0f172a !important;
    font-weight: 700 !important;
}

.gradio-container p, .gradio-container span, .gradio-container div {
    color: #334155 !important;
    line-height: 1.7 !important;
}

.gradio-container .markdown {
    color: #334155 !important;
}

.gradio-container a {
    color: #0d9488 !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.gradio-container a:hover {
    color: #14b8a6 !important;
    text-decoration: underline !important;
}

/* Hero Section */
.hero-banner {
    background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
    border-radius: 16px;
    padding: 3rem 2rem;
    margin-bottom: 3rem;
    color: white !important;
    box-shadow: 0 10px 30px rgba(13, 148, 136, 0.4);
}

.hero-banner * {
    color: white !important;
}

.hero-title {
    font-size: 3rem !important;
    font-weight: 800 !important;
    margin-bottom: 1rem !important;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    line-height: 1.2 !important;
}

.hero-subtitle {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
    opacity: 0.95;
}

.hero-description {
    font-size: 1.1rem !important;
    line-height: 1.8 !important;
    margin-bottom: 2rem !important;
    opacity: 0.9;
}

.hero-image {
    border-radius: 12px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    max-width: 100%;
    height: auto;
}

/* Stats Cards */
.stats-container {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)) !important;
    gap: 1.5rem !important;
    margin: 2rem 0 !important;
}

.stat-card {
    background: linear-gradient(135deg, #f0fdfa 0%, #ffffff 100%) !important;
    padding: 2rem 1.5rem !important;
    border-radius: 12px !important;
    text-align: center !important;
    border: 2px solid #ccfbf1 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}

.stat-card:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 8px 24px rgba(13, 148, 136, 0.2) !important;
    border-color: #14b8a6 !important;
}

.stat-number {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    color: #0d9488 !important;
    margin-bottom: 0.5rem !important;
    line-height: 1 !important;
}

.stat-label {
    font-size: 0.95rem !important;
    color: #475569 !important;
    font-weight: 600 !important;
}

/* Feature Cards */
.feature-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)) !important;
    gap: 1.5rem !important;
    margin: 2rem 0 !important;
}

.feature-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0fdfa 100%) !important;
    padding: 2rem !important;
    border-radius: 12px !important;
    border: 2px solid #ccfbf1 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}

.feature-card:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 12px 28px rgba(13, 148, 136, 0.25) !important;
    border-color: #14b8a6 !important;
}

.feature-icon {
    font-size: 2.5rem !important;
    margin-bottom: 1rem !important;
}

/* Step Cards */
.step-card {
    background: white !important;
    padding: 2rem !important;
    border-radius: 12px !important;
    margin-bottom: 1.5rem !important;
    border-left: 5px solid #14b8a6 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    transition: all 0.3s ease !important;
}

.step-card:hover {
    transform: translateX(5px) !important;
    box-shadow: 0 8px 20px rgba(13, 148, 136, 0.2) !important;
}

/* Section Headers */
.section-header {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    margin: 3rem 0 1rem 0 !important;
    text-align: center !important;
}

.section-subtitle {
    font-size: 1.1rem !important;
    color: #475569 !important;
    text-align: center !important;
    margin-bottom: 2.5rem !important;
    max-width: 800px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* CTA Buttons */
.cta-box {
    background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%) !important;
    padding: 2rem !important;
    border-radius: 12px !important;
    text-align: center !important;
    margin: 2rem 0 !important;
}

.cta-box * {
    color: white !important;
}

.cta-button {
    display: inline-block !important;
    background: white !important;
    color: #0d9488 !important;
    padding: 1rem 2.5rem !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    margin: 0.5rem !important;
    transition: all 0.3s ease !important;
    text-decoration: none !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

.cta-button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;
    color: #0d9488 !important;
}

/* Code Blocks - Fixed for Windows/iOS visibility */
.gradio-container pre {
    background: #1e293b !important;
    border-radius: 8px !important;
    padding: 1.5rem !important;
    margin: 1rem 0 !important;
    border: 1px solid #334155 !important;
    overflow-x: auto !important;
}

.gradio-container pre code {
    color: #e2e8f0 !important;
    background: transparent !important;
    font-family: 'Monaco', 'Courier New', monospace !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
}

.gradio-container code {
    background: #f1f5f9 !important;
    color: #0f172a !important;
    padding: 0.2rem 0.4rem !important;
    border-radius: 4px !important;
    font-family: 'Monaco', 'Courier New', monospace !important;
    font-size: 0.9em !important;
}

/* Accordion */
.gradio-container .accordion {
    border: 2px solid #ccfbf1 !important;
    border-radius: 12px !important;
    margin: 2rem 0 !important;
    background: white !important;
}

/* Footer */
.footer {
    text-align: center !important;
    padding: 2.5rem 0 1rem 0 !important;
    margin-top: 3rem !important;
    border-top: 2px solid #e2e8f0 !important;
}

.footer h3 {
    color: #0f172a !important;
    margin-bottom: 0.5rem !important;
}

.footer a {
    color: #0d9488 !important;
    font-weight: 600 !important;
}

.footer a:hover {
    color: #14b8a6 !important;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem !important;
    }
    
    .hero-subtitle {
        font-size: 1.2rem !important;
    }
    
    .main-content {
        padding: 2rem 1.5rem !important;
    }
    
    .stats-container,
    .feature-grid {
        grid-template-columns: 1fr !important;
    }
    
    .section-header {
        font-size: 1.8rem !important;
    }
}
"""

# Build the Gradio interface
with gr.Blocks(title="The Karen Whisperer - Reachy Mini Retail Assistant", css=custom_css) as demo:
    
    with gr.Column(elem_classes="main-content"):
        # Hero Banner
        with gr.Column(elem_classes="hero-banner"):
            gr.Markdown("# 🤖 Meet Reachy Mini", elem_classes="hero-title")
            gr.Markdown("## Your Tiny, Charming Retail Assistant", elem_classes="hero-subtitle")
            gr.Markdown(
                "**Small robot. Big patience.** Reachy Mini handles the \"Can I speak to your manager?\" "
                "so you don't have to. With AI-powered de-escalation, pattern detection, and emotional intelligence, "
                "this pint-sized assistant is revolutionizing retail customer service.",
                elem_classes="hero-description"
            )
            
            # CTA Buttons
            gr.HTML("""
            <div style="display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center; margin-top: 1.5rem;">
                <a href="https://huggingface.co/spaces/chelleboyer/reachy_mini_retail_assistant" 
                   target="_blank" class="cta-button">
                    🎮 Try Interactive Demo
                </a>
                <a href="https://thekarenwhisperer.lovable.app/" 
                   target="_blank" class="cta-button">
                    🎬 Watch Story
                </a>
                <a href="https://github.com/chelleboyer/reachy_mini_karen_whisperer" 
                   target="_blank" class="cta-button">
                    💻 View Code
                </a>
            </div>
            """)
        
        # Stats Section
        gr.HTML("""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number">99%</div>
                <div class="stat-label">De-escalation Success</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">&lt;2s</div>
                <div class="stat-label">Response Time</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Always Available</div>
            </div>
        </div>
        """)
        
        # What Reachy Can Do
        gr.Markdown("## 🚀 What Reachy Mini Can Do", elem_classes="section-header")
        gr.Markdown(
            "Customer service superpowers, minus the cape. Here's how Reachy keeps his cool while keeping customers happy.",
            elem_classes="section-subtitle"
        )
        
        gr.HTML("""
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <h3>Smart Q&A</h3>
                <p>Answers common questions about returns, prices, store hours, and policies instantly - no human needed.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🗺️</div>
                <h3>Aisle Navigation</h3>
                <p>Guides customers to the right product or aisle in seconds, reducing wait times and frustration.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3>Issue Detection</h3>
                <p>Spots out-of-stock items and inventory issues, flagging them instantly for your team.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🧘</div>
                <h3>De-escalation Pro</h3>
                <p>Calms tense situations with friendly, professional prompts designed to diffuse conflict.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🤝</div>
                <h3>Smooth Escalation</h3>
                <p>When it's actually time for a human, hands off gracefully - politely and drama-free.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Lightning Fast</h3>
                <p>Sub-2-second response times keep customers engaged and conversations flowing.</p>
            </div>
        </div>
        """)
        
        # How It Works
        gr.Markdown("## ⚙️ How It Works", elem_classes="section-header")
        gr.Markdown(
            "From \"Can I speak to your manager?\" to \"Thank you so much!\" - in three simple steps.",
            elem_classes="section-subtitle"
        )
        
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
        with gr.Accordion("🔧 Technical Architecture", open=False):
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
        gr.HTML("""
        <div class="footer">
            <h3>🤖 Reachy Mini - The Karen Whisperer</h3>
            <p style="font-size: 1.2rem; margin: 1rem 0;"><strong>Customer service with built-in chill mode.</strong></p>
            <p style="margin-top: 1.5rem;">
                <a href="https://github.com/chelleboyer/reachy_mini_karen_whisperer" target="_blank">GitHub</a> • 
                <a href="https://huggingface.co/spaces/chelleboyer/reachy_mini_karen_whisperer" target="_blank">Hugging Face</a> • 
                <a href="https://www.pollen-robotics.com/" target="_blank">Reachy Mini AI Competition</a>
            </p>
            <p style="margin-top: 1rem; color: #718096;">Made with ❤️ for retail heroes everywhere</p>
        </div>
        """)

if __name__ == "__main__":
    demo.launch()
