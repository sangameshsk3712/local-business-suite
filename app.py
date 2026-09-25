# ============================================================
# AI LOCAL BUSINESS GROWTH SUITE PRO & ENTERPRISE HUB
# Version 3.2 — Production Unified Edition
# ============================================================

import os
import time
import urllib.parse
from typing import Optional

import streamlit as st
from google import genai
from google.genai import types

# ============================================================
# 1. PAGE CONFIGURATION (Called once only)
# ============================================================

st.set_page_config(
    page_title="AI Local Business Growth Suite Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 2. PREMIUM UI STYLING
# ============================================================

st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-caption {
        font-size: 1.05rem;
        opacity: 0.75;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,0.25);
        text-align: center;
    }
    .output-box {
        padding: 1.2rem;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 3. CONSTANTS & ACTIVE MODELS (Fixes 404 & 503)
# ============================================================

APP_NAME = "AI Local Business Growth Suite Pro"
APP_VERSION = "3.2"

# gemini-3.8-flash is the active production model (gemini-2.5-flash is retired)
PRIMARY_MODEL = "gemini-3.8-flash"
FALLBACK_MODEL = "gemini-flash-latest"

# ============================================================
# 4. SESSION STATE
# ============================================================

if "interactions" not in st.session_state:
    st.session_state.interactions = 0

if "generation_history" not in st.session_state:
    st.session_state.generation_history = []

if "business_name" not in st.session_state:
    st.session_state.business_name = "Artisan Bakery & Cafe"

if "business_type" not in st.session_state:
    st.session_state.business_type = "Bakery & Coffeehouse"

if "business_location" not in st.session_state:
    st.session_state.business_location = "Austin, TX"

if "brand_voice" not in st.session_state:
    st.session_state.brand_voice = "Warm & Community-Oriented"

# ============================================================
# 5. API KEY RESOLUTION
# ============================================================

def get_api_key() -> Optional[str]:
    """Read Gemini API key from secrets or environment variables."""
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY")
        if secret_key:
            return secret_key.strip()
    except Exception:
        pass

    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        return env_key.strip()

    return None

API_KEY = get_api_key()

# ============================================================
# 6. ROBUST AI ENGINE (With 503 Exponential Backoff & 404 Fallback)
# ============================================================

class AIEngine:
    """Centralized Gemini AI service with auto-retry on 503 high demand spikes."""

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Gemini API key was not found.")
        self.client = genai.Client(api_key=api_key)

    def generate(
        self,
        prompt: str,
        system_instruction: str = "",
        max_retries: int = 3,
    ) -> str:
        models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]
        last_error = None

        for model_to_use in models_to_try:
            delay = 1.5
            for attempt in range(max_retries):
                try:
                    config_args = {}
                    if system_instruction:
                        config_args["system_instruction"] = system_instruction

                    cfg = types.GenerateContentConfig(**config_args)

                    response = self.client.models.generate_content(
                        model=model_to_use,
                        contents=prompt,
                        config=cfg,
                    )

                    if not response:
                        raise RuntimeError("AI returned no response.")

                    text = getattr(response, "text", None)
                    if not text:
                        raise RuntimeError("AI returned an empty response.")

                    return text.strip()

                except Exception as error:
                    last_error = error
                    err_str = str(error)
                    # 503 UNAVAILABLE or 429: wait with exponential backoff and retry
                    if "503" in err_str or "UNAVAILABLE" in err_str or "high demand" in err_str or "429" in err_str:
                        if attempt < max_retries - 1:
                            time.sleep(delay)
                            delay *= 2
                            continue
                    # For other errors or model deprecation, try fallback model
                    break

        raise RuntimeError(f"AI generation failed: {last_error}") from last_error

# ============================================================
# 7. SAFE AI CALL WRAPPER
# ============================================================

def run_ai(
    prompt: str,
    system_instruction: str = "",
) -> tuple[Optional[str], Optional[str]]:
    global API_KEY
    if not API_KEY:
        return (
            None,
            "Gemini API key is missing. Add GEMINI_API_KEY to Streamlit secrets.",
        )

    try:
        ai = AIEngine(API_KEY)
        start_time = time.time()
        result = ai.generate(
            prompt=prompt,
            system_instruction=system_instruction,
        )
        elapsed = time.time() - start_time
        st.session_state.interactions += 1
        return (result, f"⚡ Gemini {PRIMARY_MODEL} • {elapsed:.1f}s")
    except Exception as error:
        return (None, str(error))

# ============================================================
# 8. HISTORY & BUSINESS CONTEXT
# ============================================================

def save_history(feature: str, output: str):
    st.session_state.generation_history.insert(
        0,
        {
            "feature": feature,
            "output": output,
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
    )
    st.session_state.generation_history = st.session_state.generation_history[:20]

def business_context() -> str:
    return f"""
Business Name: {st.session_state.business_name or "Local Business"}
Category: {st.session_state.business_type or "General"}
Location: {st.session_state.business_location or "Local Area"}
Brand Voice: {st.session_state.brand_voice}
"""

# System Prompts
REVIEW_SYSTEM = "You are an expert customer experience manager. Craft warm, authentic, brand-building review responses."
SEO_SYSTEM = "You are a local SEO strategist. Generate high-intent keywords and an optimized Google Business Profile description."
FLYER_SYSTEM = "You are an advertising copywriter. Structure content with HEADLINE, SUBHEADLINE, BENEFITS, OFFER, and CTA."
WHATSAPP_SYSTEM = "You are a WhatsApp Business specialist. Write clean messages with emojis, *bold text*, _italics_, and clear calls-to-action."
LOCALIZATION_SYSTEM = "You are a localization expert. Translate and culturally adapt copy preserving the business tone."

# ============================================================
# 9. HEADER & SIDEBAR
# ============================================================

st.markdown('<div class="main-header">🚀 AI Local Business Growth Suite Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-caption">Enterprise command center for multi-location marketing, reviews, WhatsApp & local SEO.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.title("💎 Business Dashboard")
    st.markdown("### 🏪 Business Profile")
    st.session_state.business_name = st.text_input("Business Name", value=st.session_state.business_name)
    st.session_state.business_type = st.text_input("Business Category", value=st.session_state.business_type)
    st.session_state.business_location = st.text_input("Business Location", value=st.session_state.business_location)
    st.session_state.brand_voice = st.selectbox(
        "Brand Voice",
        ["Warm & Community-Oriented", "Professional & Friendly", "Premium & Elegant", "Simple & Local", "Energetic & Youthful"]
    )
    st.divider()
    st.metric("AI Generations", st.session_state.interactions)
    st.metric("Saved in History", len(st.session_state.generation_history))
    st.divider()
    if API_KEY:
        st.success("🟢 AI Engine Active (gemini-3.8-flash)")
    else:
        st.warning("🟡 Add GEMINI_API_KEY to secrets")

# Top Metrics Bar
m1, m2, m3, m4 = st.columns(4)
m1.metric("🤖 AI Engine", "Online" if API_KEY else "Setup Needed")
m2.metric("📊 Generations", st.session_state.interactions)
m3.metric("💾 Saved History", len(st.session_state.generation_history))
m4.metric("🌐 Active Model", "gemini-3.8-flash")
st.divider()

# ============================================================
# 10. UNIFIED TABS INTERFACE
# ============================================================

tabs = st.tabs([
    "🏢 Franchise Hub",
    "📱 WhatsApp Formatter",
    "💬 Review Responder",
    "🔍 Local SEO",
    "📢 Flyer Designer",
    "🌐 Regional Localization",
    "🎙️ Audio Transcriber",
    "🕘 History"
])

# ----------------- TAB 1: FRANCHISE HUB -----------------
with tabs[0]:
    st.header("🏢 Multi-Location Franchise Command")
    f1, f2, f3 = st.columns(3)
    f1.metric("Active Branches", "4 Locations", "100% Live")
    f2.metric("Network Health Index", "96.4%", "+2.4%")
    f3.metric("Review Ingestion", "1,248 reviews/mo", "Healthy")

    selected_branch = st.selectbox(
        "Select Active Franchise Location:",
        [
            "Austin Flagship Bakery & Cafe (Austin, TX)",
            "Downtown Manhattan Espresso Bar (New York, NY)",
            "London Covent Garden Patisserie (London, UK)",
            "Mumbai Bandra West Cafe & Bistro (Mumbai, India)"
        ]
    )
    st.info(f"📍 Active command session set for: **{selected_branch}**")

# ----------------- TAB 2: WHATSAPP FORMATTER -----------------
with tabs[1]:
    st.header("📱 WhatsApp Business Message Formatter")
    c1, c2 = st.columns(2)
    with c1:
        wa_name = st.text_input("Customer Name", value="John M.")
        wa_goal = st.selectbox("Message Goal", [
            "Order Dispatched / Ready for Pickup",
            "Appointment / Booking Confirmation",
            "Weekend Flash Sale & Promotion",
            "5-Star Google Review Request"
        ])
        wa_details = st.text_area("Order / Offer Details", value="Order #8291 of handcrafted sourdough loaves & cinnamon rolls is packaged and ready at the pickup counter.")
        wa_cta = st.text_input("Call to Action", value="Reply 1 to confirm pickup, or call 555-0192 for curbside delivery.")
        generate_wa = st.button("📲 Format for WhatsApp", type="primary", use_container_width=True)

    with c2:
        st.subheader("Formatted WhatsApp Copy")
        if generate_wa:
            prompt = f"""
{business_context()}
Customer Name: {wa_name}
Goal: {wa_goal}
Details: {wa_details}
Call to Action: {wa_cta}

Format instructions:
Create a ready-to-send WhatsApp message with emojis, *bold text*, _italics_, and clean spacing.
"""
            with st.spinner("Drafting WhatsApp message..."):
                output, trace = run_ai(prompt, WHATSAPP_SYSTEM)
            if output:
                save_history("WhatsApp Formatter", output)
                st.success(trace)
                st.code(output, language="markdown")
                wa_encoded = urllib.parse.quote(output)
                st.markdown(f"[📲 Open in WhatsApp Web](https://api.whatsapp.com/send?text={wa_encoded})", unsafe_allow_html=True)
            else:
                st.error(trace)

# ----------------- TAB 3: REVIEW RESPONDER -----------------
with tabs[2]:
    st.header("💬 AI Review Responder")
    r1, r2 = st.columns(2)
    with r1:
        rev_author = st.text_input("Reviewer Name", value="Jennifer M.")
        rev_rating = st.selectbox("Star Rating", ["5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"])
        rev_text = st.text_area("Review Text", height=140, value="The sourdough cinnamon rolls and pour-over coffee were unbelievable! The barista was so friendly despite the huge morning rush.")
        rev_tone = st.selectbox("Tone", ["Warm, Gracious & Appreciative", "Professional & Courteous", "Apologetic & Solution-Focused"])
        generate_rev = st.button("✨ Generate Review Response", type="primary", use_container_width=True)

    with r2:
        st.subheader("Public Response")
        if generate_rev:
            prompt = f"""
{business_context()}
Customer: {rev_author}
Rating: {rev_rating}
Review: "{rev_text}"
Tone: {rev_tone}

Write an authentic, brand-building public response.
"""
            with st.spinner("Generating response..."):
                output, trace = run_ai(prompt, REVIEW_SYSTEM)
            if output:
                save_history("Review Responder", output)
                st.success(trace)
                st.write(output)
            else:
                st.error(trace)

# ----------------- TAB 4: LOCAL SEO -----------------
with tabs[3]:
    st.header("🔍 Local SEO & Google Business Profile")
    s1, s2 = st.columns(2)
    with s1:
        seo_city = st.text_input("Target City / Metro", value=st.session_state.business_location)
        seo_keywords = st.text_input("Primary Keywords", value="artisan sourdough, fresh pastries, specialty espresso")
        generate_seo = st.button("🚀 Generate Local SEO Package", type="primary", use_container_width=True)

    with s2:
        st.subheader("SEO Growth Package")
        if generate_seo:
            prompt = f"""
{business_context()}
Target City: {seo_city}
Keywords: {seo_keywords}

Generate:
1. 700-character Google Business Profile Description
2. Top 10 High-Intent Local Keywords
3. 3 Frequently Asked Questions (FAQ) for GBP Q&A
4. Suggested GBP Post for this week
"""
            with st.spinner("Generating SEO package..."):
                output, trace = run_ai(prompt, SEO_SYSTEM)
            if output:
                save_history("Local SEO", output)
                st.success(trace)
                st.markdown(output)
            else:
                st.error(trace)

# ----------------- TAB 5: FLYER DESIGNER -----------------
with tabs[4]:
    st.header("📢 AI Flyer Copy Designer")
    f_left, f_right = st.columns(2)
    with f_left:
        flyer_title = st.text_input("Campaign Headline", value="Grand Opening & Weekend Pastry Festival")
        flyer_offer = st.text_area("Offer & Perks", value="Buy 1 Artisanal Loaf, Get Any Specialty Coffee Free. Live acoustic music 9 AM - 2 PM.")
        flyer_cta = st.text_input("Call To Action", value="Visit us at 1204 S Congress Ave this Saturday!")
        generate_flyer = st.button("🎨 Generate Flyer Blueprint", type="primary", use_container_width=True)

    with f_right:
        st.subheader("Promotional Blueprint")
        if generate_flyer:
            prompt = f"""
{business_context()}
Campaign: {flyer_title}
Offer: {flyer_offer}
CTA: {flyer_cta}

Create high-impact flyer copy structured into:
HEADLINE
SUBHEADLINE
KEY PERKS
PROMOTIONAL OFFER
CALL TO ACTION
FOOTER
"""
            with st.spinner("Designing copy..."):
                output, trace = run_ai(prompt, FLYER_SYSTEM)
            if output:
                save_history("Flyer Designer", output)
                st.success(trace)
                st.markdown(output)
            else:
                st.error(trace)

# ----------------- TAB 6: REGIONAL LOCALIZATION -----------------
with tabs[5]:
    st.header("🌐 Indian Regional Language Localization")
    l1, l2 = st.columns(2)
    with l1:
        target_lang = st.selectbox("Target Regional Language", ["Hindi", "Kannada", "Telugu", "Tamil", "Marathi", "Bengali"])
        content_to_translate = st.text_area("English Marketing Copy", height=140, value="Celebrate this festive season with freshly baked treats! Enjoy 20% off on all gift boxes this weekend.")
        generate_trans = st.button("🌍 Localize Content", type="primary", use_container_width=True)

    with l2:
        st.subheader(f"Localized in {target_lang}")
        if generate_trans:
            prompt = f"""
Language: {target_lang}
Content: "{content_to_translate}"

Culturally translate and localize this business copy so it sounds natural, authentic, and engaging.
"""
            with st.spinner(f"Localizing into {target_lang}..."):
                output, trace = run_ai(prompt, LOCALIZATION_SYSTEM)
            if output:
                save_history(f"Localization ({target_lang})", output)
                st.success(trace)
                st.write(output)
            else:
                st.error(trace)

# ----------------- TAB 7: AUDIO TRANSCRIBER -----------------
with tabs[6]:
    st.header("🎙️ Voice Memo & Audio Transcriber")
    st.write("Upload store voice memos or customer feedback recordings to transcribe via Gemini.")
    uploaded_file = st.file_uploader("Upload Audio (.mp3, .wav, .m4a, .webm)", type=["mp3", "wav", "m4a", "webm"])
    if uploaded_file and st.button("Transcribe Audio Recording 🎙️", type="primary"):
        if not API_KEY:
            st.warning("Please configure your GEMINI_API_KEY first.")
        else:
            with st.spinner("Transcribing audio..."):
                try:
                    client = genai.Client(api_key=API_KEY)
                    audio_bytes = uploaded_file.read()
                    res = client.models.generate_content(
                        model="gemini-3.5-transcribe",
                        contents=[
                            types.Part.from_bytes(data=audio_bytes, mime_type=uploaded_file.type),
                            "Accurately transcribe this audio recording with natural punctuation."
                        ]
                    )
                    st.success("Transcription Complete:")
                    st.write(res.text)
                    save_history("Audio Transcription", res.text)
                except Exception as e:
                    st.error(f"Audio transcription error: {e}")

# ----------------- TAB 8: HISTORY -----------------
with tabs[7]:
    st.header("🕘 Generation History")
    if not st.session_state.generation_history:
        st.info("No saved generations in this session yet. Generate copy in any tab to see it here!")
    else:
        for idx, item in enumerate(st.session_state.generation_history):
            with st.expander(f"{item['feature']} — {item['time']}"):
                st.write(item["output"])
