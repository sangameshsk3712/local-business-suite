import streamlit as st
import os, time, urllib.parse
from google import genai
from google.genai import types

# 1. ENTERPRISE PAGE ARCHITECTURE SETUP
st.set_page_config(page_title="AI Local Business Pro", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 2.4rem; font-weight: 800; color: #1E3A8A; margin-bottom: 0.2rem; }
    .sub-caption { font-size: 1.1rem; color: #4B5563; margin-bottom: 1.5rem; }
    .success-box { background-color: #F0FDF4; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #16A34A; margin-top: 1rem; }
    </style>
""", unsafe_allow_html=True)

# 2. STATELESS-SAFE USER TELEMETRY TRACKER
if "telemetry_actions" not in st.session_state:
    st.session_state["telemetry_actions"] = 1
else:
    st.session_state["telemetry_actions"] += 1

st.sidebar.title("💎 Enterprise Dashboard")
st.sidebar.metric(label="Total App Interactions", value=st.session_state["telemetry_actions"])
st.sidebar.markdown("---")

st.markdown("<div class='main-header'>🚀 AI-Powered Local Business Growth Suite Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-caption'>Elite, self-healing automation engine empowering local community businesses.</div>", unsafe_allow_html=True)

# 3. ADVANCED FAULT-TOLERANT MODEL PIPELINES
MODEL_TIER_1 = 'gemini-2.5-flash'
MODEL_TIER_2 = 'gemini-1.5-flash'

active_key = None
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
    active_key = st.secrets["GEMINI_API_KEY"].strip()
    client = genai.Client(api_key=active_key)
else:
    st.sidebar.header("🔑 Authentication Matrix")
    user_key = st.sidebar.text_input("Enter Production API Token (AQ...):", type="password")
    if user_key:
        active_key = user_key.strip()
        client = genai.Client(api_key=active_key)
    else:
        st.stop()

# 4. UNIVERSAL SELF-HEALING ROUTING UTILITY
# 4. UNIVERSAL SELF-HEALING ROUTING UTILITY
def run_inference(prompt_data, sys_instruction=None):
    full_prompt = f"{sys_instruction}\n\nTask: {prompt_data}" if sys_instruction else prompt_data
    
    # Dynamic live sync connection matrix
    try:
        if "GEMINI_API_KEY" in st.secrets:
            local_client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"].strip())
        elif active_key:
            local_client = genai.Client(api_key=active_key)
        else:
            local_client = client
    except Exception:
        local_client = client

    for model_node, label in [(MODEL_TIER_1, "Alpha Channel"), (MODEL_TIER_2, "Beta Circuit")]:
        try:
            res = local_client.models.generate_content(model=model_node, contents=full_prompt)
            if res and res.text:
                return res.text, f"⚡ Active via {label} ({model_node})"
        except Exception as err:
            time.sleep(0.5)
            continue
    return None, "All infrastructure pipelines currently saturated. Please check your API key validity and retry."

APP_URL = "https://streamlit.app"
VIRAL_FT = f"\n\n⚡ Generated via AI Growth Suite. Try Free: {APP_URL}"

# 5. SEVEN-TAB ENGINE INTERFACE INITIALIZATION
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💬 Review Assistant", "🔍 SEO Optimizer", "📢 Flyer Designer",
    "📱 WhatsApp Formatter", "🌐 Regional Studio", "📊 Competitor Intel", "🎬 Reels Scriptwriter"
])

with tab1:
    st.header("💬 Strategic Review Management Matrix")
    c1, c2 = st.columns(2)
    with c1:
        b_name = st.text_input("Business Name", placeholder="e.g., Shiva Bakery", key="k1")
        rating = st.selectbox("Rating Received", ["5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"], key="k2")
        rev_txt = st.text_area("Paste Review Text Here:", key="k3")
        tone = st.selectbox("Brand Voice", ["Professional & Grateful", "Apologetic & Solution-Oriented"], key="k4")
        btn1 = st.button("Generate Public Response", key="b1")
    with c2:
        st.subheader("Optimized Public Output")
        if btn1:
            if not rev_txt:
                st.warning("Please provide the review text.")
            else:
                with st.spinner("Processing sentiment matrix..."):
                    p = f"PR Manager for '{b_name}'. Rating: {rating}. Review: '{rev_txt}'. Style: '{tone}'. If 3 stars or lower, insert an escalation clause inviting private mediation."
                    out, trace = run_inference(p, "You are a professional corporate PR Executive.")
                    if out: 
                        st.markdown(f"<div class='success-box'><b>Status:</b> {trace}</div>", unsafe_allow_html=True)
                        st.write(out + VIRAL_FT)
                    else:
                        st.error(trace)

with tab2:
    st.header("🔍 Hyper-Local SEO Performance Bundle")
    c1, c2 = st.columns(2)
    with c1:
        niche = st.text_input("Operational Vertical Niche", placeholder="e.g., Electrical Contractor", key="k5")
        loc = st.text_input("Target Location City Name", placeholder="e.g., Kalaburagi, Karnataka", key="k6")
        topic = st.text_input("Campaign Focus Topic", placeholder="e.g., Festival season promotion", key="k7")
        btn2 = st.button("Compile Advanced Search Metadata", key="b2")
    with c2:
        st.subheader("Optimized Search Engine Packages")
        if btn2:
            if not niche or not loc:
                st.warning("Please provide business type and location details.")
            else:
                with st.spinner("Injecting geo-locational strings..."):
                    p = f"Compile local SEO suite for a '{niche}' in '{loc}' targeting '{topic}'. Provide: 1. A Google Business Profile post update under 1500 chars with CTA. 2. Array of 10 hyper-local meta keywords."
                    out, trace = run_inference(p, "You are an elite Local SEO Engineer.")
                    if out: 
                        st.markdown(f"<div class='success-box'><b>Status:</b> {trace}</div>", unsafe_allow_html=True)
                        st.write(out + VIRAL_FT)
                    else:
                        st.error(trace)

with tab3:
    st.header("📢 Graphic Copy Structural Blueprint")
    c1, c2 = st.columns(2)
    with c1:
        goal = st.text_input("Campaign Title Milestone", placeholder="e.g., Grand Inauguration", key="k8")
        details = st.text_area("Value Matrices Parameters", placeholder="e.g., 50% discount this Saturday", key="k9")
        btn3 = st.button("Structure Graphic Composition Script", key="b3")
    with c2:
        st.subheader("Structured Typography Framework")
        if btn3:
            if not goal:
                st.warning("Please provide a campaign destination milestone goal.")
            else:
                with st.spinner("Processing visual hierarchy weight..."):
                    p = f"Design a visual copywriting wireframe flyer layout for Goal: '{goal}', Parameters: '{details}'. Structure cleanly for Canva copy-pasting into: VISUAL ANCHOR HEADLINE, SUBHEADER, MODULAR BLOCK DATA, CTA FOOTER."
                    out, trace = run_inference(p, "You are an award-winning Graphic Layout Copywriter.")
                    if out: 
                        st.markdown(f"<div class='success-box'><b>Status:</b> {trace}</div>", unsafe_allow_html=True)
                        st.write(out + VIRAL_FT)
                    else:
                        st.error(trace)

with tab4:
    st.header("📱 Direct-Response WhatsApp Message Formatter")
    c1, c2 = st.columns(2)
    with c1:
        wa_in = st.text_area("Raw Promotional Update Copy", placeholder="e.g., Fresh mangoes available today.", key="k10")
        wa_cta = st.text_input("Direct Transaction Action Variable (CTA)", placeholder="e.g., WhatsApp reply or call 9999999999", key="k11")
        btn4 = st.button("Format Enterprise WhatsApp Script", key="b4")
    with c2:
        st.subheader("Copy-Paste Script Output")
        if btn4:
            if not wa_in:
                st.warning("Please enter update details.")
            else:
                with st.spinner("Constructing engagement chat patterns..."):
                    p = f"Format text into an enterprise WhatsApp broadcast: '{wa_in}' with CTA trigger: '{wa_cta}'. Maximize spacing, use bold formatting (*text*), and decorate with visual emojis."
                    out, trace = run_inference(p, "You are an expert Mobile Conversion Copywriter.")
                    if out:
                        f_out = out + VIRAL_FT
                        st.success(f"Status: {trace}")
                        st.code(f_out, language="text")
                        encoded = urllib.parse.quote(f_out)
                        st.markdown(f'<a href="https://whatsapp.com{encoded}" target="_blank"><button style="width:100%;background-color:#25D366;color:white;border:none;padding:0.75rem;border-radius:0.4rem;font-weight:bold;cursor:pointer;">📲 Fast Forward Direct to WhatsApp Contacts</button></a>', unsafe_allow_html=True)
                    else:
                        st.error(trace)

with tab5:
    st.header("🌐 Regional Semantic Translation Studio")
    c1, c2 = st.columns(2)
    with c1:
        t_lang = st.selectbox("Target Regional Linguistic Node", ["Kannada (ಕನ್ನಡ)", "Hindi (ಹಿन्दी)", "Telugu (తెలుగు)", "Marathi (ಮರಾठी)"], key="k12")
        lang_in = st.text_area("Source English Marketing Copy:", placeholder="Enter marketing text here...", key="k13")
        btn5 = st.button("Process Linguistic Localization Strategy", key="b5")
    with c2:
        st.subheader("Localized Regional Copy Output")
        if btn5:
            if not lang_in:
                st.warning("Please input english source marketing properties text.")
            else:
                with st.spinner(f"Executing localization matrix for {t_lang}..."):
                    p = f"Translate and culturally localize this business marketing copy: '{lang_in}' into natural, persuasive {t_lang} meant for local commerce. Do not do a literal machine translation."
                    out, trace = run_inference(p, f"You are a native copywriting strategist fluent in {t_lang}.")
                    if out: 
                        st.markdown(f"<div class='success-box'><b>Status:</b> {trace}</div>", unsafe_allow_html=True)
