"""Prediction engine: EfficientNetB0 feature extraction + ANN + RAG + Groq."""
from __future__ import annotations

import os
import re
import warnings
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import joblib
import numpy as np
import streamlit as st
from PIL import Image

# ── Disease metadata ──────────────────────────────────────────────────────────
SEVERITY_MAP: dict[str, str] = {
    "healthy": "Low", "scab": "Moderate", "rot": "High", "rust": "Moderate",
    "blight": "High", "mildew": "Moderate", "spot": "Moderate",
    "curl": "Moderate", "mosaic": "High", "canker": "High",
    "mite": "Moderate", "virus": "High", "bacterial": "High",
}


def _severity(raw: str) -> str:
    r = raw.lower()
    for kw, sev in SEVERITY_MAP.items():
        if kw in r:
            return sev
    return "Moderate"


def _parse_class(raw: str) -> tuple[str, str]:
    """Split 'Apple___Apple_scab' → ('Apple', 'Apple Scab')."""
    parts = raw.split("___", 1)
    plant = parts[0].replace("_", " ").replace("(", "").replace(")", "").strip()
    plant = re.sub(r"\s+", " ", plant)
    disease = parts[1].replace("_", " ").strip() if len(parts) > 1 else plant
    disease = re.sub(r"\s+", " ", disease)
    return plant, disease


# ── Model loaders (cached) ────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading ANN model…")
def _load_ann_v2():
    import tensorflow as tf
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    ann = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(1280,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(38, activation='softmax')
    ])
    ann.load_weights(os.path.join(model_dir, "ann_model.keras"))
    scaler = joblib.load(os.path.join(model_dir, "scaler.pkl"))
    le = joblib.load(os.path.join(model_dir, "label_encoder.pkl"))
    return ann, scaler, le


@st.cache_resource(show_spinner="Loading EfficientNetB0…")
def _load_efnet():
    import tensorflow as tf
    base = tf.keras.applications.EfficientNetB0(
        weights="imagenet", include_top=False, pooling="avg"
    )
    base.trainable = False
    return base


@st.cache_resource(show_spinner="Loading FAISS index…")
def _load_vectorstore():
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )
    rag_dir = os.path.join(os.path.dirname(__file__), "rag", "policy_index")
    return FAISS.load_local(rag_dir, embeddings, allow_dangerous_deserialization=True)


# ── Predict ───────────────────────────────────────────────────────────────────
def predict_disease(img: Image.Image) -> dict:
    """Run EfficientNetB0 feature extraction → scaler → ANN prediction."""
    from tensorflow.keras.applications.efficientnet import preprocess_input

    ann, scaler, le = _load_ann_v2()
    efnet = _load_efnet()

    img_resized = img.resize((224, 224))
    arr = np.array(img_resized, dtype=np.float32)
    arr = preprocess_input(arr)
    arr = np.expand_dims(arr, axis=0)

    features = efnet.predict(arr, verbose=0)
    features_scaled = scaler.transform(features)

    probs = ann.predict(features_scaled, verbose=0)[0]
    top_idx = int(np.argmax(probs))
    confidence = float(probs[top_idx])
    raw_class = le.classes_[top_idx]
    plant, disease = _parse_class(raw_class)

    return {
        "raw_class": raw_class, "plant": plant, "disease": disease,
        "confidence": confidence, "severity": _severity(raw_class),
        "top5": [
            {"class": le.classes_[i], "prob": float(probs[i])}
            for i in np.argsort(probs)[::-1][:5]
        ],
    }


# ── Groq LLM ──────────────────────────────────────────────────────────────────
def _groq_complete(messages: list[dict], temperature: float = 0.4,
                   max_tokens: int = 512) -> str:
    """Call Groq Chat Completions with a full message list."""
    from groq import Groq
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY", "")
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()


def _simple_complete(prompt: str, system: str = "") -> str:
    """Single prompt + optional system → response."""
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": prompt})
    return _groq_complete(msgs)


# ── Treatment advice (RAG + Groq) ─────────────────────────────────────────────
def get_advice(raw_class: str, confidence: float) -> dict:
    """Retrieve RAG docs and generate farmer-friendly treatment advice."""
    vs = _load_vectorstore()

    query = f"treatment and management for {raw_class.replace('___', ' ').replace('_', ' ')}"
    docs_scores = vs.similarity_search_with_score(query, k=4)
    context = "\n\n".join(d.page_content for d, _ in docs_scores)

    seen = set()
    sources = []
    for d, _ in docs_scores:
        name = d.metadata.get("source", "Unknown")
        if name not in seen:
            seen.add(name)
            sources.append({"name": name})

    plant, disease = _parse_class(raw_class)
    is_healthy = "healthy" in raw_class.lower()

    if is_healthy:
        prompt = (
            f"The plant ({plant}) appears healthy with {confidence:.1%} confidence. "
            f"Based on these agricultural guidelines:\n{context}\n\n"
            f"Provide exactly 4 simple, practical tips a farmer can follow to keep "
            f"this plant healthy. Use easy-to-understand language. "
            f"Return as a numbered list only. No introduction or conclusion."
        )
    else:
        prompt = (
            f"A farmer's {plant} crop has been diagnosed with {disease} "
            f"(confidence: {confidence:.1%}).\n"
            f"Agricultural knowledge base:\n{context}\n\n"
            f"Give exactly 5 clear, actionable treatment steps that a farmer "
            f"can follow immediately. Use simple language — avoid scientific jargon. "
            f"Each step should be 1-2 sentences max. Include what to apply, "
            f"how much, and when if possible.\n"
            f"Return as a numbered list only. No introduction or conclusion."
        )

    system = (
        "You are AgroVision AI, a trusted agriculture advisor who speaks to farmers "
        "in simple, clear language. Your advice must be practical and based on "
        "the retrieved agricultural guidelines. Focus on what a farmer can do "
        "right now with commonly available materials. Always prioritise organic "
        "and low-cost solutions first, then chemical treatments if needed."
    )

    raw_advice = _simple_complete(prompt, system=system)

    tips = []
    for line in raw_advice.split("\n"):
        line = re.sub(r"^\s*\d+[\.)\-]\s*", "", line).strip()
        line = re.sub(r"^\*+\s*", "", line).strip()
        if line and len(line) > 5:
            tips.append(line)
    if not tips:
        tips = [raw_advice]

    return {"advice": tips[:6], "sources": sources}


# ── RAG Chatbot (with conversation memory) ────────────────────────────────────
def rag_chat(question: str, context_disease: str = "",
             chat_history: list[dict] | None = None) -> str:
    """RAG chatbot with conversation memory — conversational, not a summarizer."""
    vs = _load_vectorstore()

    # Build retrieval query
    query = question
    if context_disease:
        disease_readable = context_disease.replace("___", " ").replace("_", " ")
        query = f"{question} regarding {disease_readable}"

    docs_scores = vs.similarity_search_with_score(query, k=3)
    rag_context = "\n".join(f"- {d.page_content}" for d, _ in docs_scores)
    sources = list({d.metadata.get("source", "Unknown") for d, _ in docs_scores})

    # Disease context
    disease_note = ""
    if context_disease:
        disease_note = (
            f"The farmer recently detected: "
            f"{context_disease.replace('___', ' — ').replace('_', ' ')}. "
        )

    # ── System prompt: personality FIRST, reference LAST ──────────────
    system = (
        "You are AgroVision AI, a smart agriculture assistant.\n\n"
        "RULES (follow strictly):\n"
        "1. Answer ONLY what the farmer asked. Do NOT give unsolicited info.\n"
        "2. Be conversational — talk like a helpful friend, not a textbook.\n"
        "3. Keep answers SHORT: 2-4 sentences for simple questions, up to 6 for complex ones.\n"
        "4. Never start with 'Based on the guidelines...' or 'According to...' — just answer directly.\n"
        "5. If the farmer asks a follow-up, refer to what you already discussed — don't repeat.\n"
        "6. Prefer organic/cheap solutions first. Mention chemical only if asked or necessary.\n"
        "7. Use the reference notes below as background knowledge, but do NOT summarize or list them.\n\n"
        f"{disease_note}\n"
        f"Reference notes (use as background, do NOT quote or summarize these):\n{rag_context}"
    )

    messages = [{"role": "system", "content": system}]

    # Inject past conversation turns for memory
    if chat_history:
        for msg in chat_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "assistant" and "───" in content:
                content = content.split("───")[0].strip()
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": question})

    answer = _groq_complete(messages, temperature=0.5, max_tokens=300)

    # Source attribution
    if sources:
        src_str = " · ".join(sources)
        answer += f"\n\n───\n📚 {src_str}"

    return answer
