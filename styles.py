"""CSS styles for AgroVision AI dashboard."""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global Reset ──────────────────────────────────────────────────── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #050a14; color: #c9d1d9; }
section[data-testid="stSidebar"] { display: none; }
header[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 1rem 2rem 2rem !important; max-width: 1200px; }

/* ── Animated Background Particles ─────────────────────────────────── */
.stApp::before {
    content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background:
        radial-gradient(ellipse 600px 400px at 10% 20%, rgba(16,185,129,0.05) 0%, transparent 70%),
        radial-gradient(ellipse 500px 500px at 90% 80%, rgba(59,130,246,0.04) 0%, transparent 70%),
        radial-gradient(ellipse 400px 300px at 50% 50%, rgba(139,92,246,0.03) 0%, transparent 70%);
    pointer-events: none; z-index: 0;
    animation: bgShift 12s ease-in-out infinite alternate;
}
@keyframes bgShift {
    0%   { opacity: 0.6; }
    50%  { opacity: 1; }
    100% { opacity: 0.7; }
}

/* ── Keyframes ─────────────────────────────────────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(16,185,129,0.15); }
    50%      { box-shadow: 0 0 35px rgba(16,185,129,0.30); }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes borderGlow {
    0%, 100% { border-color: #1e3a5f; }
    50%      { border-color: #10b98166; }
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-6px); }
}

/* ── Header ────────────────────────────────────────────────────────── */
.av-header {
    background: linear-gradient(135deg, #0a1628 0%, #0f1d36 40%, #0a1628 100%);
    border: 1px solid #1a2744; border-radius: 20px;
    padding: 32px 36px; margin-bottom: 24px;
    display: flex; align-items: center; gap: 22px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
    position: relative; overflow: hidden;
    animation: fadeInUp 0.7s ease-out;
}
.av-header::before {
    content: ''; position: absolute; top: -60%; right: -15%;
    width: 350px; height: 350px; border-radius: 50%;
    background: radial-gradient(circle, rgba(16,185,129,0.08) 0%, transparent 70%);
    animation: float 6s ease-in-out infinite;
}
.av-header::after {
    content: ''; position: absolute; bottom: -40%; left: -10%;
    width: 250px; height: 250px; border-radius: 50%;
    background: radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%);
    animation: float 8s ease-in-out infinite reverse;
}
.av-logo {
    width: 60px; height: 60px; border-radius: 16px;
    background: linear-gradient(135deg, #064e3b, #10b981);
    display: flex; align-items: center; justify-content: center;
    font-size: 30px; flex-shrink: 0;
    box-shadow: 0 6px 24px rgba(16,185,129,0.3);
    animation: pulseGlow 3s ease-in-out infinite;
}
.av-title {
    font-size: 1.65rem; font-weight: 800; color: #f0f6fc;
    letter-spacing: -0.5px; margin: 0;
    background: linear-gradient(135deg, #f0f6fc 0%, #10b981 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.av-subtitle { font-size: 0.82rem; color: #6b7b8d; margin-top: 4px; line-height: 1.5; }
.av-badge {
    display: inline-block; background: linear-gradient(135deg, #064e3b, #10b981);
    color: #d1fae5; font-size: 0.65rem; font-weight: 700;
    padding: 3px 10px; border-radius: 20px; margin-left: 8px;
    letter-spacing: 0.8px; text-transform: uppercase;
    animation: pulseGlow 2.5s ease-in-out infinite;
}

/* ── Tabs ──────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0; background: #0a1020; border-radius: 14px;
    padding: 5px; border: 1px solid #1a2744; margin-bottom: 22px;
    animation: fadeInUp 0.8s ease-out;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #6b7b8d; border: none;
    border-radius: 10px; padding: 11px 24px; font-size: 0.85rem;
    font-weight: 600; transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
}
.stTabs [data-baseweb="tab"]:hover {
    color: #a5b4c4; background: rgba(16,185,129,0.05);
}
.stTabs [aria-selected="true"] {
    color: #e6edf3 !important;
    background: linear-gradient(135deg, #064e3b, #047857) !important;
    box-shadow: 0 4px 18px rgba(16,185,129,0.3);
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 0 !important; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ── Cards ─────────────────────────────────────────────────────────── */
.av-card {
    background: linear-gradient(145deg, #0c1527 0%, #0a1020 100%);
    border: 1px solid #1e293b; border-radius: 16px;
    padding: 24px; margin-bottom: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    animation: fadeInUp 0.6s ease-out both;
    position: relative; overflow: hidden;
}
.av-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(16,185,129,0.3), transparent);
    opacity: 0; transition: opacity 0.3s;
}
.av-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    border-color: #10b98133;
}
.av-card:hover::before { opacity: 1; }
.av-card-title {
    display: flex; align-items: center; gap: 10px;
    font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.2px; color: #10b981; margin-bottom: 16px;
    padding-bottom: 12px; border-bottom: 1px solid #1e293b;
}

/* ── Upload Area ───────────────────────────────────────────────────── */
.av-upload {
    background: linear-gradient(145deg, #0c1527 0%, #0a1020 100%);
    border: 2px dashed #10b98133; border-radius: 16px;
    padding: 24px; text-align: center;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    animation: borderGlow 4s ease-in-out infinite;
}
.av-upload:hover {
    border-color: #10b98188;
    box-shadow: 0 0 30px rgba(16,185,129,0.08);
}
.av-upload-icon { font-size: 2.8rem; margin-bottom: 8px; animation: float 4s ease-in-out infinite; }
.av-upload-text { font-size: 0.85rem; color: #6b7b8d; }

/* ── Disease Badge ─────────────────────────────────────────────────── */
.av-disease-badge {
    background: linear-gradient(135deg, #0a2818 0%, #052e16 100%);
    border: 1px solid #166534; border-radius: 14px;
    padding: 20px; margin-bottom: 16px;
    animation: fadeInUp 0.5s ease-out;
    position: relative; overflow: hidden;
}
.av-disease-badge::after {
    content: ''; position: absolute; top: 0; right: 0; width: 80px; height: 80px;
    background: radial-gradient(circle, rgba(16,185,129,0.1) 0%, transparent 70%);
}
.av-disease-name { font-size: 1.3rem; font-weight: 800; color: #4ade80; }
.av-plant-name { font-size: 0.82rem; color: #6b8f71; margin-top: 3px; }

/* ── Metrics ───────────────────────────────────────────────────────── */
.av-metrics { display: flex; gap: 14px; margin: 16px 0; flex-wrap: wrap; }
.av-metric {
    background: #070c16; border: 1px solid #1e293b; border-radius: 12px;
    padding: 16px 18px; flex: 1; min-width: 100px;
    transition: all 0.3s ease;
    animation: fadeInUp 0.7s ease-out both;
}
.av-metric:hover {
    border-color: #10b98144;
    box-shadow: 0 0 20px rgba(16,185,129,0.1);
}
.av-metric-label { font-size: 0.68rem; color: #6b7b8d; text-transform: uppercase;
    letter-spacing: 1px; font-weight: 600; }
.av-metric-value { font-size: 1.5rem; font-weight: 800; color: #f0f6fc; margin-top: 4px;
    background: linear-gradient(135deg, #f0f6fc, #10b981);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Progress Bar ──────────────────────────────────────────────────── */
.av-progress-bg {
    background: #1e293b; border-radius: 8px; height: 10px;
    margin-top: 8px; overflow: hidden;
}
.av-progress-fill {
    height: 100%; border-radius: 8px;
    background: linear-gradient(90deg, #064e3b, #10b981, #34d399);
    background-size: 200% 100%;
    animation: shimmer 2.5s linear infinite;
    box-shadow: 0 0 16px rgba(16,185,129,0.4);
}

/* ── Severity Badges ───────────────────────────────────────────────── */
.sev-mild { background: #052e16; color: #4ade80; border: 1px solid #166534;
    padding: 5px 16px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; display: inline-block; }
.sev-moderate { background: #431407; color: #fb923c; border: 1px solid #9a3412;
    padding: 5px 16px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; display: inline-block; }
.sev-severe { background: #450a0a; color: #f87171; border: 1px solid #991b1b;
    padding: 5px 16px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; display: inline-block; }

/* ── Advice Items ──────────────────────────────────────────────────── */
.av-advice-item {
    display: flex; gap: 12px; align-items: flex-start;
    padding: 12px 0; border-bottom: 1px solid #1e293b15;
    font-size: 0.88rem; color: #c9d1d9; line-height: 1.6;
    transition: all 0.25s ease;
}
.av-advice-item:hover {
    padding-left: 8px;
    border-bottom-color: #10b98122;
}
.av-advice-icon { font-size: 1.15rem; flex-shrink: 0; margin-top: 2px; }

/* ── Source Tags ────────────────────────────────────────────────────── */
.av-source-tag {
    display: inline-flex; align-items: center; gap: 8px;
    background: #0c1527; border: 1px solid #1e293b; border-radius: 12px;
    padding: 10px 16px; margin: 4px; font-size: 0.82rem; color: #9ca3af;
    transition: all 0.3s ease;
}
.av-source-tag:hover {
    border-color: #10b98155;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.av-source-dot { width: 8px; height: 8px; border-radius: 50%; background: #10b981; flex-shrink: 0;
    box-shadow: 0 0 6px rgba(16,185,129,0.5);
}

/* ── Detect Button ─────────────────────────────────────────────────── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #064e3b 0%, #047857 50%, #10b981 100%) !important;
    color: white !important; border: none !important; border-radius: 14px !important;
    padding: 14px !important; font-size: 1rem !important; font-weight: 700 !important;
    box-shadow: 0 6px 24px rgba(16,185,129,0.3);
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important; letter-spacing: 0.3px;
    position: relative; overflow: hidden;
}
.stButton > button::before {
    content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.5s ease;
}
.stButton > button:hover::before { left: 100%; }
.stButton > button:hover {
    box-shadow: 0 8px 32px rgba(16,185,129,0.5) !important;
    transform: translateY(-2px);
}
.stButton > button:active { transform: translateY(0); }

/* ── Chat Bubbles ──────────────────────────────────────────────────── */
.av-chat-user {
    background: linear-gradient(135deg, #0c1527, #111d33);
    border-left: 3px solid #10b981;
    border-radius: 0 14px 14px 0; padding: 16px 20px;
    margin-bottom: 14px; font-size: 0.88rem;
    animation: fadeInUp 0.3s ease-out;
}
.av-chat-bot {
    background: linear-gradient(135deg, #0a1020, #0f172a);
    border-left: 3px solid #3b82f6;
    border-radius: 0 14px 14px 0; padding: 16px 20px;
    margin-bottom: 14px; font-size: 0.88rem; color: #c9d1d9;
    animation: fadeInUp 0.3s ease-out;
}
.av-chat-label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; margin-bottom: 6px; }
.av-chat-label-u { color: #10b981; }
.av-chat-label-b { color: #3b82f6; }

/* ── Info Box ──────────────────────────────────────────────────────── */
.av-info {
    background: linear-gradient(145deg, #0c1527, #0a1020);
    border: 1px solid #1e293b;
    border-radius: 14px; padding: 20px 24px; font-size: 0.85rem;
    color: #6b7b8d; line-height: 1.7;
    transition: border-color 0.3s;
}
.av-info:hover { border-color: #10b98133; }

/* ── Inputs ────────────────────────────────────────────────────────── */
.stTextInput input, .stTextArea textarea {
    background: #0c1527 !important; color: #e6edf3 !important;
    border: 1px solid #1e293b !important; border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 3px rgba(16,185,129,0.12) !important;
}

/* ── Suggested prompts ─────────────────────────────────────────────── */
.av-prompt-btn {
    display: inline-block; background: #0c1527; border: 1px solid #1e293b;
    border-radius: 22px; padding: 8px 18px; font-size: 0.78rem;
    color: #6b7b8d; margin: 4px; cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
}
.av-prompt-btn:hover {
    border-color: #10b981; color: #10b981;
    box-shadow: 0 0 16px rgba(16,185,129,0.1);
    transform: translateY(-1px);
}

/* ── Footer ────────────────────────────────────────────────────────── */
.av-footer {
    text-align: center; padding: 28px 0 10px; color: #374151;
    font-size: 0.75rem; border-top: 1px solid #1e293b; margin-top: 36px;
    letter-spacing: 0.3px;
}

/* ── Stats Grid (About Tab) ────────────────────────────────────────── */
.av-stat-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 14px; margin: 16px 0;
}
.av-stat-box {
    background: #070c16; border: 1px solid #1e293b; border-radius: 14px;
    padding: 18px; text-align: center;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    animation: fadeInUp 0.6s ease-out both;
}
.av-stat-box:hover {
    border-color: #10b98144;
    transform: translateY(-3px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.3);
}
.av-stat-value {
    font-size: 1.6rem; font-weight: 800;
    background: linear-gradient(135deg, #f0f6fc, #10b981);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.av-stat-label { font-size: 0.7rem; color: #6b7b8d; text-transform: uppercase;
    letter-spacing: 1px; font-weight: 600; margin-top: 4px; }
.av-stat-sub { font-size: 0.72rem; color: #4b5563; margin-top: 4px; }

/* ── Best Model Highlight ──────────────────────────────────────────── */
.av-best-model {
    background: linear-gradient(135deg, #064e3b22, #10b98111);
    border: 1px solid #10b98133; border-radius: 16px;
    padding: 22px; text-align: center; margin: 18px 0;
    animation: pulseGlow 3s ease-in-out infinite;
}
.av-best-model-title { font-size: 0.72rem; color: #6b8f71; text-transform: uppercase;
    letter-spacing: 1.5px; font-weight: 700; }
.av-best-model-name { font-size: 1.8rem; font-weight: 800; color: #4ade80;
    margin: 6px 0; }
.av-best-model-acc { font-size: 1.1rem; color: #a7f3d0; font-weight: 600; }

/* ── Streamlit overrides ───────────────────────────────────────────── */
.stFileUploader > div { border-radius: 14px !important; }
.stSpinner > div { color: #10b981 !important; }
div[data-testid="stImage"] { border-radius: 14px; overflow: hidden; }

/* Plotly chart dark background override */
.js-plotly-plot .plotly .main-svg { border-radius: 12px; }
</style>
"""
