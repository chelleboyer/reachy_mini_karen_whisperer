"""
The Karen Whisperer - Reachy Mini Retail Assistant
HF Spaces landing page styled to match https://thekarenwhisperer.lovable.app/
"""
import gradio as gr

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --bg: #f7f8fb;
    --grid: rgba(0, 0, 0, 0.04);
    --text: #0b0b0d;
    --muted: #4b4b52;
    --accent: #0bb4c6;
}

.gradio-container {
    font-family: 'Manrope', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
}

.page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    background-color: var(--bg);
    background-image:
        linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px);
    background-size: 60px 60px;
    position: relative;
}

.content {
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
    padding: 48px 32px 56px;
}

.badge-row {
    margin-bottom: 18px;
}

.hf-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: white;
    border-radius: 999px;
    padding: 10px 14px;
    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.08);
    font-weight: 700;
    color: var(--muted);
    border: 1px solid rgba(0, 0, 0, 0.06);
}

.hero {
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    gap: 32px;
    align-items: center;
}

.headline h1 {
    font-size: 3rem;
    line-height: 1.05;
    margin: 0 0 14px 0;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.headline .accent {
    color: var(--accent);
}

.headline h2 {
    font-size: 1.5rem;
    margin: 0 0 12px 0;
    font-weight: 600;
    color: var(--text);
}

.headline p {
    margin: 0 0 18px 0;
    font-size: 1.05rem;
    color: var(--muted);
    line-height: 1.55;
}

.hero-actions {
    display: flex;
    gap: 14px;
    margin: 18px 0 28px 0;
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 14px 20px;
    border-radius: 14px;
    font-weight: 700;
    font-size: 1rem;
    text-decoration: none;
    transition: transform 0.15s ease, box-shadow 0.2s ease;
    border: none;
}

.btn.primary {
    background: linear-gradient(135deg, #089db3, #0bc2cf);
    color: white;
    box-shadow: 0 10px 30px rgba(11, 180, 198, 0.25);
}

.btn.ghost {
    background: white;
    color: var(--text);
    border: 1px solid rgba(0, 0, 0, 0.08);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.btn:hover {
    transform: translateY(-1px);
}

.stats {
    display: grid;
    grid-template-columns: repeat(3, minmax(120px, 1fr));
    gap: 18px;
    margin-top: 10px;
}

.stat-card {
    background: rgba(255, 255, 255, 0.6);
    border-radius: 14px;
    padding: 18px;
    border: 1px solid rgba(0, 0, 0, 0.06);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.04);
    display: grid;
    gap: 6px;
}

.stat-card .value {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--text);
}

.stat-card .label {
    color: var(--muted);
    font-weight: 600;
    font-size: 0.95rem;
}

.device-frame {
    background: white;
    border-radius: 20px;
    box-shadow: 0 25px 80px rgba(0, 0, 0, 0.15);
    padding: 10px;
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.device-inner {
    position: relative;
    overflow: hidden;
    border-radius: 16px;
    background: linear-gradient(180deg, rgba(0,0,0,0.02), rgba(0,0,0,0.05));
}

.device-inner img {
    display: block;
    width: 100%;
    height: auto;
}

.slider-dots {
    display: flex;
    justify-content: center;
    gap: 6px;
    padding: 12px 0 4px 0;
}

.slider-dots span {
    width: 8px;
    height: 8px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 999px;
}

.slider-dots span.active {
    background: var(--text);
    width: 18px;
}

@media (max-width: 980px) {
    .hero {
        grid-template-columns: 1fr;
    }
    .headline h1 {
        font-size: 2.4rem;
    }
    .content {
        padding: 32px 20px 40px;
    }
}
"""


with gr.Blocks(title="The Karen Whisperer", css=custom_css, theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_classes="page"):
        with gr.Column(elem_classes="content"):
            gr.HTML("""
            <div class="badge-row">
                <span class="hf-badge">Powered by Hugging Face</span>
            </div>
            """)

            with gr.Row(elem_classes="hero"):
                with gr.Column():
                    gr.HTML("""
                    <div class="headline">
                        <h1>Meet <span class="accent">Reachy Mini</span></h1>
                        <h2>Retail Assistant</h2>
                        <p>Your tiny, charming Retail Assistant—aka the Karen Whisperer.</p>
                        <p>Small robot. Big patience. De-escalation with built-in chill mode—he handles the "Can I speak to your manager?" so you don't have to.</p>
                        <div class="hero-actions">
                            <a class="btn primary" href="https://huggingface.co/spaces/chelleboyer/reachy_mini_karen_whisperer" target="_blank" rel="noopener">Try Reachy Mini</a>
                            <a class="btn ghost" href="https://huggingface.co/spaces/chelleboyer/reachy_mini_karen_whisperer" target="_blank" rel="noopener">Vote on Hugging Face</a>
                        </div>
                    </div>
                    """)

                    gr.HTML("""
                    <div class="stats">
                        <div class="stat-card"><div class="value">99%</div><div class="label">De-escalation Rate</div></div>
                        <div class="stat-card"><div class="value">&lt;2s</div><div class="label">Response Time</div></div>
                        <div class="stat-card"><div class="value">24/7</div><div class="label">Always On</div></div>
                    </div>
                    """)

                with gr.Column():
                    gr.HTML("""
                    <div class="device-frame">
                        <div class="device-inner">
                            <img src="https://raw.githubusercontent.com/chelleboyer/reachy_mini_karen_whisperer/main/images/1-reachy-mini-retail-assistant.PNG" alt="Reachy Mini assistant">
                        </div>
                        <div class="slider-dots">
                            <span></span><span class="active"></span><span></span><span></span><span></span><span></span><span></span>
                        </div>
                    </div>
                    """)

if __name__ == "__main__":
    demo.launch()
