"""AgroVision AI — Plant Disease Detection & AI Advisor."""
from __future__ import annotations
import os, warnings
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from styles import CSS

load_dotenv()

st.set_page_config(
    page_title="AgroVision AI — Plant Disease Detection & AI Advisor",
    page_icon="🌿", layout="wide", initial_sidebar_state="collapsed",
)
st.markdown(CSS, unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="av-header">
  <div class="av-logo">🌿</div>
  <div>
    <div class="av-title">AgroVision AI <span class="av-badge">v1.1</span></div>
    <div class="av-subtitle">Detect plant diseases instantly using AI and receive smart treatment guidance.</div>
  </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔬 Leaf Disease Detection", "💬 RAG Chatbot", "📊 About & Evaluation"])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — Detection
# ══════════════════════════════════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns([1, 1.5], gap="large")

    with col_l:
        st.markdown("""<div class="av-upload">
          <div class="av-upload-icon">📸</div>
          <div class="av-upload-text">Upload a clear photo of the plant leaf</div>
        </div>""", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload", type=["jpg","jpeg","png","webp"],
                                    label_visibility="collapsed", key="leaf_up")
        if uploaded:
            img = Image.open(uploaded).convert("RGB")
            st.image(img, use_container_width=True, caption="Uploaded leaf")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        detect = st.button("🔬 Detect Disease & Get Advice", key="detect")

    with col_r:
        if detect and uploaded:
            with st.spinner("🔬 Analysing leaf…"):
                from predict import predict_disease, get_advice
                result = predict_disease(img)

            plant, disease, conf = result["plant"], result["disease"], result["confidence"]
            sev = result["severity"]
            sev_cls = {"Low":"sev-mild","Moderate":"sev-moderate","High":"sev-severe"}.get(sev,"sev-moderate")
            sev_lbl = {"Low":"Mild","Moderate":"Moderate","High":"Severe"}.get(sev,"Moderate")
            healthy = "healthy" in disease.lower()

            # ── Card 1: Detection Result ───────────────────────────
            st.markdown(f"""
            <div class="av-disease-badge">
              <div class="av-plant-name">🌱 {plant}</div>
              <div class="av-disease-name">{'✅ Healthy' if healthy else '⚠️ ' + disease}</div>
            </div>
            <div class="av-metrics">
              <div class="av-metric">
                <div class="av-metric-label">Confidence</div>
                <div class="av-metric-value">{conf:.1%}</div>
                <div class="av-progress-bg"><div class="av-progress-fill" style="width:{conf*100:.0f}%"></div></div>
              </div>
              <div class="av-metric">
                <div class="av-metric-label">Severity</div>
                <div style="margin-top:8px"><span class="{sev_cls}">● {sev_lbl}</span></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Card 2: Treatment Advice ───────────────────────────
            with st.spinner("🤖 Generating treatment advice…"):
                advice_data = get_advice(result["raw_class"], conf)

            tip_icons = ["🌿","💧","🧴","✂️","🛡️","📋"]
            st.markdown('<div class="av-card"><div class="av-card-title">💊 What To Do — Treatment Steps</div>', unsafe_allow_html=True)
            for i, tip in enumerate(advice_data["advice"]):
                ic = tip_icons[i % len(tip_icons)]
                st.markdown(f'<div class="av-advice-item"><span class="av-advice-icon">{ic}</span><span>{tip}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Cards 3 & 4: Prevention + Safety side-by-side ─────────
            col_prev, col_safe = st.columns(2)

            with col_prev:
                prev_tips = [
                    ("🔄", "Rotate your crops each season to break disease cycles"),
                    ("🌾", "Choose disease-resistant seed varieties from trusted sources"),
                    ("💧", "Water at the base of the plant — avoid wetting the leaves"),
                    ("👁️", "Check your plants weekly for spots, wilting, or colour changes"),
                ]
                st.markdown('<div class="av-card"><div class="av-card-title">🛡️ Prevention Tips</div>', unsafe_allow_html=True)
                for ic, t in prev_tips:
                    st.markdown(f'<div class="av-advice-item"><span class="av-advice-icon">{ic}</span><span>{t}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_safe:
                safety = [
                    ("🧤", "Wear gloves and a mask before spraying any treatment"),
                    ("📏", "Use the exact amount written on the pesticide label"),
                    ("🌿", "Try neem oil or bio-pesticides before chemical sprays"),
                    ("🚿", "Wash hands and equipment thoroughly after every use"),
                ]
                st.markdown('<div class="av-card"><div class="av-card-title">⚠️ Safety Reminders</div>', unsafe_allow_html=True)
                for ic, t in safety:
                    st.markdown(f'<div class="av-advice-item"><span class="av-advice-icon">{ic}</span><span>{t}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ── Card 5: Sources ────────────────────────────────────
            if advice_data.get("sources"):
                src_html = ''.join(
                    f'<span class="av-source-tag"><span class="av-source-dot"></span>{s["name"]}</span>'
                    for s in advice_data["sources"]
                )
                st.markdown(
                    f'<div class="av-card"><div class="av-card-title">📚 Advice Based On</div>'
                    f'{src_html}</div>',
                    unsafe_allow_html=True,
                )

            st.session_state["last_disease"] = result["raw_class"]

        elif detect and not uploaded:
            st.warning("⚠️ Please upload a leaf image first.")
        elif not detect:
            st.markdown("""<div class="av-info">
              <strong style="color:#f0f6fc;">🌿 How does it work?</strong><br><br>
              <b>Step 1:</b> Take a clear photo of the sick leaf and upload it here<br>
              <b>Step 2:</b> Our AI scans the leaf and identifies the disease<br>
              <b>Step 3:</b> It checks trusted farming guides (ICAR, FAO, WHO)<br>
              <b>Step 4:</b> You get easy-to-follow treatment advice instantly
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — RAG Chatbot
# ══════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(
        '<p style="color:#6b7b8d;font-size:0.85rem;margin:8px 0 16px;">'
        'Ask the <strong style="color:#10b981;">RAG-powered advisor</strong> anything about '
        'plant diseases, treatments, and farming practices. Answers are grounded in '
        'ICAR, FAO-IPM & WHO guidelines via FAISS retrieval.</p>',
        unsafe_allow_html=True,
    )

    ctx = st.session_state.get("last_disease", "")
    if ctx:
        st.markdown(
            f'<div class="av-info">🔗 Disease context from detection: '
            f'<strong style="color:#10b981;">{ctx.replace("___"," — ").replace("_"," ")}</strong></div>',
            unsafe_allow_html=True,
        )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="av-chat-user"><div class="av-chat-label av-chat-label-u">👤 You</div>{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="av-chat-bot"><div class="av-chat-label av-chat-label-b">🤖 AgroVision AI RAG</div>{msg["content"]}</div>',
                unsafe_allow_html=True,
            )

    # Suggested prompts when empty
    if not st.session_state.chat_history:
        st.markdown(
            '<div style="margin:16px 0 12px;color:#6b7b8d;font-size:0.82rem;">Try asking:</div>'
            '<div>'
            '<span class="av-prompt-btn">🩺 How to treat this disease?</span>'
            '<span class="av-prompt-btn">🌿 Organic treatment options?</span>'
            '<span class="av-prompt-btn">🛡️ How to prevent future infection?</span>'
            '<span class="av-prompt-btn">🌾 Best crop rotation practices?</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    # Chat input using a form so it clears properly on submit
    with st.form(key="chat_form", clear_on_submit=True):
        q = st.text_input(
            "Message",
            placeholder="Ask AgroVision AI about your crop…",
            label_visibility="collapsed",
        )
        col_send, col_clear, _ = st.columns([1, 1, 4])
        with col_send:
            submitted = st.form_submit_button("Send ➤", use_container_width=True)
        with col_clear:
            clear = st.form_submit_button("🗑️ Clear", use_container_width=True)

    if clear:
        st.session_state.chat_history = []
        st.rerun()

    if submitted and q.strip():
        st.session_state.chat_history.append({"role": "user", "content": q})
        with st.spinner("🤖 Retrieving from FAISS & generating answer…"):
            from predict import rag_chat
            ans = rag_chat(
                q,
                context_disease=ctx,
                chat_history=st.session_state.chat_history[:-1],  # all except current msg
            )
        st.session_state.chat_history.append({"role": "assistant", "content": ans})
        st.rerun()

# ══════════════════════════════════════════════════════════════════════
# TAB 3 — About
# ══════════════════════════════════════════════════════════════════════
with tab3:
    import plotly.graph_objects as go

    st.markdown("""
    <div class="av-card"><div class="av-card-title">🌿 About AgroVision AI</div>
      <p style="color:#9ca3af;line-height:1.7;font-size:0.9rem;">
        AgroVision AI is a premium, state-of-the-art plant disease detection & agricultural advisory system. 
        It integrates deep learning feature extraction with retrieval-augmented generation (RAG) to deliver 
        accurate, context-aware diagnoses and action-oriented farming solutions grounded in international agronomy standards.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Best Model Highlights & Overall stats
    st.markdown("""
    <div class="av-best-model">
      <div class="av-best-model-title">⭐️ Overall Best Model</div>
      <div class="av-best-model-name">Artificial Neural Network (ANN)</div>
      <div class="av-best-model-acc">Accuracy: 95.99%</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="av-stat-box">
          <div class="av-stat-value">Logistic Regression</div>
          <div class="av-stat-label">Best ML Classifier</div>
          <div class="av-stat-sub">Accuracy: 95.86%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="av-stat-box">
          <div class="av-stat-value">K-Means</div>
          <div class="av-stat-label">Best Clustering Model</div>
          <div class="av-stat-sub">Silhouette Score: 0.3014</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="av-stat-box">
          <div class="av-stat-value">EfficientNetB0</div>
          <div class="av-stat-label">Feature Extractor</div>
          <div class="av-stat-sub">ImageNet Pre-trained</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Side-by-side charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Classifier Models Accuracy Chart
        classifiers = ["Logistic Regression", "Linear SVM", "Gradient Boosting", "K-Nearest Neighbors", "Random Forest", "Extra Trees"]
        classifier_accs = [95.86, 94.75, 91.76, 90.96, 89.85, 89.09]

        fig_cls = go.Figure(go.Bar(
            x=classifier_accs,
            y=classifiers,
            orientation='h',
            marker=dict(
                color=classifier_accs,
                colorscale=[[0, '#064e3b'], [0.5, '#059669'], [1, '#10b981']],
                line=dict(color='#1e293b', width=1)
            ),
            text=[f"{val}%" for val in classifier_accs],
            textposition='auto',
            textfont=dict(color='white', size=11, family='Inter'),
            hoverinfo='x+y'
        ))
        fig_cls.update_layout(
            title=dict(
                text="Machine Learning Classifiers (Accuracy %)",
                font=dict(color='#f0f6fc', size=14, family='Inter')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title=dict(text="Accuracy (%)", font=dict(color='#6b7b8d', family='Inter')),
                showgrid=True,
                gridcolor='#1e293b',
                tickfont=dict(color='#6b7b8d', family='Inter'),
                range=[80, 100]
            ),
            yaxis=dict(
                autorange="reversed",
                tickfont=dict(color='#e6edf3', family='Inter')
            ),
            margin=dict(l=10, r=10, t=40, b=10),
            height=340,
        )
        st.plotly_chart(fig_cls, use_container_width=True, config={'displayModeBar': False})

    with chart_col2:
        # Neural Network models
        nns = ["ANN Accuracy", "DNN Accuracy", "CNN Accuracy"]
        nn_accs = [95.99, 61.84, 53.68]

        fig_nn = go.Figure(go.Bar(
            x=nns,
            y=nn_accs,
            marker=dict(
                color=nn_accs,
                colorscale=[[0, '#1e3a8a'], [0.5, '#3b82f6'], [1, '#60a5fa']],
                line=dict(color='#1e293b', width=1)
            ),
            text=[f"{val}%" for val in nn_accs],
            textposition='auto',
            textfont=dict(color='white', size=11, family='Inter'),
            hoverinfo='x+y'
        ))
        fig_nn.update_layout(
            title=dict(
                text="Deep Learning Architectures (Accuracy %)",
                font=dict(color='#f0f6fc', size=14, family='Inter')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(
                title=dict(text="Accuracy (%)", font=dict(color='#6b7b8d', family='Inter')),
                showgrid=True,
                gridcolor='#1e293b',
                tickfont=dict(color='#6b7b8d', family='Inter'),
                range=[0, 100]
            ),
            xaxis=dict(
                tickfont=dict(color='#e6edf3', family='Inter')
            ),
            margin=dict(l=10, r=10, t=40, b=10),
            height=340,
        )
        st.plotly_chart(fig_nn, use_container_width=True, config={'displayModeBar': False})

    # Tech stack details card
    st.markdown("""
    <div class="av-card"><div class="av-card-title">🧠 Model Architecture Details</div>
      <div class="av-advice-item"><span class="av-advice-icon">📷</span><span><strong style="color:#f0f6fc;">Feature Extraction:</strong> EfficientNetB0 (pre-trained on ImageNet) → 1280-dimensional embedding vector representation</span></div>
      <div class="av-advice-item"><span class="av-advice-icon">🧠</span><span><strong style="color:#f0f6fc;">Classifier:</strong> Artificial Neural Network (Dense layers: 128 → 64 → 32 → 38 output classes with Softmax activation)</span></div>
      <div class="av-advice-item"><span class="av-advice-icon">📚</span><span><strong style="color:#f0f6fc;">RAG Framework:</strong> FAISS Vector Index + HuggingFace Local MiniLM Embeddings + Groq LLaMA-3.1 8B Instant</span></div>
      <div class="av-advice-item"><span class="av-advice-icon">🌾</span><span><strong style="color:#f0f6fc;">Train Dataset:</strong> PlantVillage Dataset — 38 distinct classes (diseased and healthy) across 14 crop species</span></div>
    </div>
    <div class="av-card"><div class="av-card-title">📚 Trusted Knowledge Sources</div>
      <span class="av-source-tag"><span class="av-source-dot"></span>ICAR — Indian Council of Agricultural Research</span>
      <span class="av-source-tag"><span class="av-source-dot"></span>FAO — Integrated Pest Management Guides</span>
      <span class="av-source-tag"><span class="av-source-dot"></span>WHO — Pesticide Classification & Safety Guidelines</span>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('<div class="av-footer">🌿 AgroVision AI · Built with Streamlit · Powered by Groq + FAISS</div>', unsafe_allow_html=True)
