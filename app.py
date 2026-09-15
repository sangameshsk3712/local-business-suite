import streamlit as st
import os
import time
import urllib.parse
from google import genai
from google.genai import types

# =====================================================================
# 1. ENTERPRISE PAGE ARCHITECTURE & PERFORMANCE STYLING
# =====================================================================
st.set_page_config(
    page_title="AI Local Business Growth Suite Pro",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; font-weight: 800; color: #1E3A8A; margin-bottom: 0.2rem; }
    .sub-caption { font-size: 1.1rem; color: #4B5563; margin-bottom: 2rem; }
    .success-box { background-color: #F0FDF4; padding: 1.2rem; border-radius: 0.5rem; border-left: 5px solid #16A34A; margin-top: 1rem; }
    .viral-badge { background-color: #EFF6FF; padding: 0.5rem; border-radius: 0.3rem; border: 1px dashed #3B82F6; font-size: 0.85rem; margin-top: 0.5rem; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. STATELESS-SAFE USER TELEMETRY TRACKER
# =====================================================================
if "system_telemetry_actions" not in st.session_state:
    st.session_state["system_telemetry_actions"] = 1
else:
    st.session_state["system_telemetry_actions"] += 1

st.sidebar.title("💎 Enterprise Dashboard")
st.sidebar.markdown("### 📊 System Telemetry")
st.sidebar.metric(label="Total App Interactions", value=st.session_state["system_telemetry_actions"])
st.sidebar.markdown("---")

st.markdown("<div class='main-header'>🚀 AI-Powered Local Business Growth Suite Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-caption'>Elite, fault-tolerant automation engine empowering micro-enterprises and local community businesses.</div>", unsafe_allow_html=True)

# =====================================================================
# 3. MULTI-TIER SELF-HEALING INFRASTRUCTURE PIPELINE
# =====================================================================
MODEL_ALPHA = 'gemini-2.5-flash'
MODEL_BETA  = 'gemini-1.5-flash'
MODEL_GAMMA = 'gemini-1.5-pro'

# =====================================================================
# 4. SECURE AGNOSTIC KEY RESOLUTION LAYER
# =====================================================================
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
    client = genai.Client()
else:
    st.sidebar.header("🔑 Cryptographic Authentication")
    user_key = st.sidebar.text_input("Enter Production API Token (AQ...):", type="password")
    if user_key:
        os.environ["GEMINI_API_KEY"] = user_key.strip()
        client = genai.Client()
    else:
        st.stop()

# =====================================================================
# 5. SELF-HEALING INFERENCE ROUTING UTILITY
# =====================================================================
def execute_core_inference(prompt_payload, system_instruction_set=None):
    config_args = {}
    if system_instruction_set:
        config_args["config"] = types.GenerateContentConfig(system_instruction=system_instruction_set, temperature=0.7)
    else:
        config_args["config"] = types.GenerateContentConfig(temperature=0.7)

    for model_node, label in [(MODEL_ALPHA, "Alpha Channel"), (MODEL_BETA, "Beta Circuit"), (MODEL_GAMMA, "Gamma Failover")]:
        try:
            response = client.models.generate_content(model=model_node, contents=prompt_payload, **config_args)
            return response.text, f"⚡ Active via {label} ({model_node})"
        except Exception:
            time.sleep(0.5)
            continue
            
    return None, "All endpoints saturated. Please re-trigger the generation button in 15 seconds."

APP_URL = "https://streamlit.app"
VIRAL_FOOTPRINT = f"\n\n⚡ Generated via AI Growth Suite. Try Free: {APP_URL}"

# =====================================================================
# 6. SEVEN-TAB ELITE APPLICATION ENGINE INTERFACE
# =====================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💬 Review Reply Assistant", 
    "🔍 Local SEO Optimizer", 
    "📢 Smart Flyer Layout Designer",
    "📱 WhatsApp Broadcast Formatter",
    "🌐 Regional Language Studio",
    "📊 Competitor Intel Matrix",
    "🎬 Social Video Scriptwriter"
])
# ---------------------------------------------------------------------
# TAB 1: REVIEW REPLY MATRIX
# ---------------------------------------------------------------------
with tab1:
    st.header("💬 Strategic Review Management Matrix")
    st.write("Neutralize customer escalations and synthesize professional public-facing responses.")
    col1, col2 = st.columns(2)
    with col1:
        biz_name = st.text_input("Corporate / Business Entity Name", placeholder="e.g., Shiva Bakery", key="m1_name")
        rating = st.selectbox("Customer Sentiment Rating", ["5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"], key="m1_rank")
        review_text = st.text_area("Inbound Unstructured Review Copy:", placeholder="Paste text here...", key="m1_copy")
        tone = st.selectbox("Brand Voice Matrix", ["Professional & Grateful", "Apologetic & Solution-Oriented", "Friendly & Casual"], key="m1_voice")
        generate_reply = st.button("Generate Public Response Blueprint", key="btn_m1")
    with col2:
        st.subheader("Optimized Public Output")
        if generate_reply and review_text:
            with st.spinner("Executing sequence processing..."):
                sys_inst = "You are a professional corporate PR Executive specializing in brand preservation."
                prompt = f"Analyze review for '{biz_name}'. Stars: {rating}. Review: '{review_text}'. Style: {tone}. If 3 stars or lower, insert an escalation clause inviting private mediation."
                payload_response, log_trace = execute_core_inference(prompt, sys_inst)
                if payload_response:
                    st.markdown(f"<div class='success-box'><b>System Status:</b> {log_trace}</div>", unsafe_allow_html=True)
                    st.write(payload_response + VIRAL_FOOTPRINT)

# ---------------------------------------------------------------------
# TAB 2: GEOGRAPHIC SEO COMPILER
# ---------------------------------------------------------------------
with tab2:
    st.header("🔍 Hyper-Local SEO Performance Bundle")
    st.write("Optimize localization search context variables to isolate geographic traffic.")
    col1, col2 = st.columns(2)
    with col1:
        biz_type = st.text_input("Operational Vertical Niche", placeholder="e.g., Electrical Contractor", key="m2_niche")
        city_location = st.text_input("Target Regional Demographics / City Node", placeholder="e.g., Kalaburagi, Karnataka", key="m2_geo")
        seo_topic = st.text_input("Campaign Focus Variable", placeholder="e.g., Festival season promotion", key="m2_focus")
        generate_seo = st.button("Compile Advanced Search Metadata", key="btn_m2")
    with col2:
        st.subheader("Optimized Search Engine Packages")
        if generate_seo and biz_type and city_location:
            with st.spinner("Injecting semantic geo-locational indexing strings..."):
                sys_inst = "You are an elite Local Search Engine Optimization (SEO) Engineer."
                prompt = f"Compile local SEO suite for '{biz_type}' in '{city_location}' targeting '{seo_topic}'. Provide a Google Business post under 1500 chars and 10 hyper-local keywords."
                payload_response, log_trace = execute_core_inference(prompt, sys_inst)
                if payload_response:
                    st.markdown(f"<div class='success-box'><b>System Status:</b> {log_trace}</div>", unsafe_allow_html=True)
                    st.write(payload_response + VIRAL_FOOTPRINT)

# ---------------------------------------------------------------------
# TAB 3: TYPOGRAPHICAL FLYER DESIGNER
# ---------------------------------------------------------------------
with tab3:
    st.header("📢 Graphic Copy Structural Blueprint")
    st.write("Enforce advertising hierarchy configurations to build structured visual print scripts.")
    col1, col2 = st.columns(2)
    with col1:
        flyer_goal = st.text_input("Campaign Destination Milestone", placeholder="e.g., Grand Inauguration", key="m3_mile")
        offer_details = st.text_area("Value Matrices & Promotional Parameters", placeholder="e.g., 50% discount this Saturday", key="m3_params")
        generate_flyer = st.button("Structure Graphic Composition Script", key="btn_m3")
    with col2:
        st.subheader("Structured Typography Framework")
        if generate_flyer and flyer_goal:
            with st.spinner("Processing visual weight variables..."):
                sys_inst = "You are an award-winning Graphic Layout Copywriter."
                prompt = f"Design a visual copywriting wireframe flyer layout for Goal: '{flyer_goal}' and Parameters: '{offer_details}'. Break text down cleanly into VISUAL ANCHOR HEADLINE, SUBHEADER, MODULAR DATA, and CALL TO ACTION FOOTER."
                payload_response, log_trace = execute_core_inference(prompt, sys_inst)
                if payload_response:
                    st.markdown(f"<div class='success-box'><b>System Status:</b> {log_trace}</div>", unsafe_allow_html=True)
                    st.write(payload_response + VIRAL_FOOTPRINT)

# ---------------------------------------------------------------------
# TAB 4: WHATSAPP BROADCAST SCALER
# ---------------------------------------------------------------------
with tab4:
    st.header("📱 Direct-Response WhatsApp Message Formatter")
    st.write("Convert flat text into copy sequences designed for WhatsApp broadcasting.")
    col1, col2 = st.columns(2)
    with col1:
        wa_update = st.text_area("Raw Promotional Update Parameters", placeholder="e.g., Fresh mangoes available at wholesale prices today.", key="m4_input")
        wa_cta = st.text_input("Direct Transaction Action Variable (CTA)", placeholder="e.g., WhatsApp reply or call 9999999999", key="m4_cta")
        generate_wa = st.button("Format Enterprise WhatsApp Script", key="btn_m4")
    with col2:
        st.subheader("Copy-Paste Script Output")
        if generate_wa and wa_update:
            with st.spinner("Constructing engagement broadcast patterns..."):
                sys_inst = "You are an expert Mobile Conversion Copywriter."
                prompt = f"Format this text into an enterprise WhatsApp broadcast message: '{wa_update}' using CTA trigger: '{wa_cta}'. Maximize line spacing, use markdown bolding (*text*), and decorate with visual emojis."
                payload_response, log_trace = execute_core_inference(prompt, sys_inst)
                if payload_response:
                    final_output = payload_response + VIRAL_FOOTPRINT
                    st.success(f"System Status: {log_trace}")
                    st.code(final_output, language="text")
                    
                    encoded_text = urllib.parse.quote(final_output)
                    wa_share_url = f"https://whatsapp.com{encoded_text}"
                    st.markdown(f'<a href="{wa_share_url}" target="_blank" style="text-decoration:none;"><button style="width:100%;background-color:#25D366;color:white;border:none;padding:0.75rem;border-radius:0.4rem;font-weight:bold;cursor:pointer;font-size:1rem;margin-top:0.5rem;">📲 Fast Forward Direct to WhatsApp Contacts</button></a>', unsafe_allow_html=True)
                    st.markdown("<div class='viral-badge'>💡 Sharing propagates your free application trace link organically across regional networks.</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# TAB 5: REGIONAL SUITE LOCALIZATION
# ---------------------------------------------------------------------
with tab5:
    st.header("🌐 Regional Semantic Translation Studio")
    st.write("Translate standard English campaign properties into localized regional dialects.")
    col1, col2 = st.columns(2)
    with col1:
        target_lang = st.selectbox("Target Regional Linguistic Node", ["Kannada (ಕನ್ನಡ)", "Hindi (ಹಿन्दी)", "Telugu (తెలుగు)", "Marathi (ಮರಾಠಿ)"], key="m5_lang")
        input_marketing_text = st.text_area("Source English Marketing Properties:", placeholder="Enter marketing text here...", key="m5_src")
        generate_translation = st.button("Process Linguistic Localization Strategy", key="btn_m5")
    with col2:
        st.subheader("Localized Regional Copy Output")
        if generate_translation and input_marketing_text:
            with st.spinner(f"Executing localization matrix mapping for {target_lang}..."):
                sys_inst = f"You are a native linguistic expert and copywriting strategist fluent in {target_lang}."
                prompt = f"Translate and adapt this business marketing copy: '{input_marketing_text}' into natural, highly persuasive {target_lang} meant for local commerce. Do not do a literal machine translation."
                payload_response, log_trace = execute_core_inference(prompt, sys_inst)
                if payload_response:
                    st.markdown(f"<div class='success-box'><b>System Status:</b> {log_trace}</div>", unsafe_allow_html=True)
                    st.write(payload_response + VIRAL_FOOTPRINT)

# ---------------------------------------------------------------------
# TAB 6: COMPETITOR INTELLIGENCE MATRIX
# ---------------------------------------------------------------------
with tab6:
    st.header("📊 AI Competitor Intelligence Matrix")
    st.write("Analyze your local competitor's advertising methods and generate strategies to outperform them.")
    col1, col2 = st.columns(2)
    with col1:
        comp_text = st.text_area("Paste Competitor's Offer / Social Post / Ad copy here:", placeholder="e.g., Mega Bakery offering birthday cakes at 20% discount with free delivery...")
        my_advantage = st.text_input("Your Business Strength", placeholder="e.g., We use 100% organic ingredients, live baking display")
        generate_intel = st.button("Generate Counter Strategy", key="btn_m6")
    with col2:
        st.subheader("Counter-Marketing Blueprint")
        if generate_intel and comp_text:
            with st.spinner("Analyzing competitor strategy vectors..."):
# ---------------------------------------------------------------------
# TAB 7: INSTAGRAM & SOCIAL REELS SCRIPTWRITER
# ---------------------------------------------------------------------
with tab7:
    st.header("🎬 Smart Instagram & Social Reels Scriptwriter")
    st.write("Generate high-retention short video scripts to grow your local social media presence organically.")
    col1, col2 = st.columns(2)
    with col1:
        video_topic = st.text_input("What is your video about?", placeholder="e.g., A day in the life of a bakery, hidden plumbing tips, unboxing new inventory", key="m7_topic")
        video_style = st.selectbox("Video Concept Style", ["Educational & Informative", "Fast-Paced & Energetic", "Storytelling & Emotional"], key="m7_style")
        generate_script = st.button("Generate Video Blueprint", key="btn_m7")
    with col2:
        st.subheader("Social Reel Script Structure")
        if generate_script and video_topic:
            with st.spinner("Architecting visual timeline hooks..."):
                sys_inst = "You are a viral Social Media Content Director and Short-Form Video Algorithm Consultant."
                prompt = f"Create a viral 30-second video script outline for an Instagram Reel or YouTube Short about: '{video_topic}' using a '{video_style}' presentation model. Provide exactly: 1. A High-Retention Opening Hook string (0-3 seconds). 2. Visual Scene-by-Scene directions matched with corresponding voiceover scripts. 3. High-reach optimized text tags (#hashtags)."
                payload_response, log_trace = execute_core_inference(prompt, sys_inst)
                if payload_response:
                    st.markdown(f"<div class='success-box'><b>System Status:</b> {log_trace}</div>", unsafe_allow_html=True)
                    st.write(payload_response + VIRAL_FOOTPRINT)
