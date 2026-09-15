import streamlit as st
import os
from google import genai

# 1. PAGE SETUP & THEME CONFIGURATION
st.set_page_config(
    page_title="AI Local Business Growth Suite",
    page_icon="🚀",
    layout="wide"
)

# 2. BULLETPROOF NATIVE SESSION STATE ANALYTICS
if "total_user_actions" not in st.session_state:
    st.session_state["total_user_actions"] = 1
else:
    st.session_state["total_user_actions"] += 1

# Render persistent statistics in the sidebar
st.sidebar.title("📈 System Metrics")
st.sidebar.metric(label="Total App Interactions", value=st.session_state["total_user_actions"])
st.sidebar.markdown("---")

# Main Page Titles
st.title("🚀 AI-Powered Local Business Growth Suite")
st.caption("Production-grade automation tools empowering local shops, freelancers, and small businesses.")

# 3. ADVANCED DISASTER RECOVERY & DUAL-MODEL ARCHITECTURE
# Utilizing Google's recommended production-tier endpoints
PRIMARY_MODEL = 'gemini-3.6-flash'
BACKUP_MODEL = 'gemini-2.5-pro'

# 4. SECURE AUTHENTICATION SUB-SYSTEM (Supports New AQ. Key Structures)
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
    client = genai.Client()
else:
    st.sidebar.header("🔑 Authentication Matrix")
    user_key = st.sidebar.text_input("Enter Gemini API Key (AQ...):", type="password")
    st.sidebar.markdown("💡 *Generate a free key at [Google AI Studio](https://google.com)*")
    if user_key:
        os.environ["GEMINI_API_KEY"] = user_key.strip()
        client = genai.Client()
    else:
        st.info("← Please configure your Gemini API Key in the sidebar or via Streamlit Secrets to begin.")
        st.stop()

# 5. CORE WORKFLOW ENGINE (SELF-HEALING API WRAPPER)
def run_safely_with_fallback(prompt_text):
    """
    Executes a prompt against the primary model. If the server throws a 503, 
    overloads, or rate limits, it automatically intercepts the fault and handles 
    execution via the heavy-duty backup tier.
    """
    try:
        # Primary Pipeline Execution
        response = client.models.generate_content(
            model=PRIMARY_MODEL,
            contents=prompt_text
        )
        return response.text, "Primary Server"
    except Exception as primary_error:
        # Failover Interception Mechanics
        try:
            response = client.models.generate_content(
                model=BACKUP_MODEL,
                contents=prompt_text
            )
            return response.text, "Failover Backup Server"
        except Exception as secondary_error:
            # Complete Pipeline Outage Containment
            return None, f"Outage Control Triggered. Primary: {str(primary_error)} | Backup: {str(secondary_error)}"


# 6. APPLICATION TAB LAYOUT DASHBOARD
tab1, tab2, tab3 = st.tabs([
    "💬 Review Reply Assistant", 
    "🔍 Local SEO Bundle", 
    "📢 Smart Flyer Designer"
])

# =====================================================================
# TAB 1: REVIEW REPLY ASSISTANT (Brand Reputation Optimization)
# =====================================================================
with tab1:
    st.header("💬 Review Reply Assistant")
    st.write("Convert online reviews into professional, brand-building customer retention loops.")
    
    col1, col2 = st.columns(2)
    with col1:
        biz_name = st.text_input("Business Name", placeholder="e.g., Shiva Bakery", key="t1_biz")
        rating = st.selectbox("Star Rating Received", ["⭐⭐⭐⭐⭐ (5 Stars)", "⭐⭐⭐⭐ (4 Stars)", "⭐⭐⭐ (3 Stars)", "⭐⭐ (2 Stars)", "⭐ (1 Star)"], key="t1_rate")
        review_text = st.text_area("Paste Customer Review Text Here:", key="t1_txt")
        tone = st.selectbox("Response Strategy", ["Professional & Grateful", "Apologetic & Solution-Oriented", "Friendly & Casual"], key="t1_tone")
        
        generate_reply = st.button("Generate Response Blueprint", key="btn_reply")
        
    with col2:
        st.subheader("System Response Output")
        if generate_reply and review_text:
            with st.spinner("Analyzing text sentiment and structuring reply..."):
                prompt = f"""
                Act as an elite corporate PR and Customer Relations Manager for '{biz_name}'.
                Generate a ready-to-copy public response to a customer who left a {rating} review.
                The review says: "{review_text}"
                Adopt a strict '{tone}' communication style. 
                If the review rating is 3 stars or lower, provide a formal, polite escalation clause inviting them to resolve the dispute privately with management via email/phone. Do not include template bracket placeholders; output production-ready text.
                """
                output_text, routing_info = run_safely_with_fallback(prompt)
                
                if output_text:
                    st.success(f"Generation Complete ({routing_info})")
                    st.write(output_text)
                else:
                    st.error("❌ High-demand infrastructure block encountered.")
                    st.warning("Google's public free-tier endpoints are fully occupied. Please retry in 30 seconds.")

# =====================================================================
# TAB 2: LOCAL SEO BUNDLE GENERATOR (Regional Search Ranking)
# =====================================================================
with tab2:
    st.header("🔍 Local SEO Bundle Optimizer")
    st.write("Generate keyword-optimized Google Business Profile updates to rank #1 in localized searches.")
    
    col1, col2 = st.columns(2)
    with col1:
        biz_type = st.text_input("Business Type / Niche", placeholder="e.g., Plumber, Organic Café, Gym", key="t2_type")
        city_location = st.text_input("Target Location / City Name", placeholder="e.g., Kalaburagi, Karnataka", key="t2_loc")
        seo_topic = st.text_input("Core Marketing Objective / Topic", placeholder="e.g., 20% festival discount, new arrivals, weekend hours", key="t2_obj")
        
        generate_seo = st.button("Compile SEO Optimization Bundle", key="btn_seo")
        
    with col2:
        st.subheader("SEO Content Package")
        if generate_seo and biz_type and city_location:
            with st.spinner("Injecting geo-targeted metadata strings..."):
                prompt = f"""
                Act as a world-class Local SEO marketing strategist.
                Compile a comprehensive local SEO bundle for a '{biz_type}' operating out of '{city_location}'.
                The campaign objective is: '{seo_topic}'.
                
                Provide exactly two distinct deliverable modules:
                1. A high-converting Google Business Profile (GBP) update post (under 1500 characters). Ensure it organically matches regional semantic keywords, uses engagement hooks, and finishes with a strong Call-To-Action (CTA).
                2. A curated index of 10 high-intent, hyper-local target keywords they should embed within their website's meta tags to isolate search intent in '{city_location}'.
                """
                output_text, routing_info = run_safely_with_fallback(prompt)
                
                if output_text:
                    st.success(f"Compilation Complete ({routing_info})")
                    st.write(output_text)
                else:
                    st.error("❌ High-demand infrastructure block encountered.")
                    st.warning("Google's public free-tier endpoints are fully occupied. Please retry in 30 seconds.")

# =====================================================================
# TAB 3: SMART FLYER DESIGNER (Copywriting Layout Architecture)
# =====================================================================
with tab3:
    st.header("📢 Smart Flyer Visual Copywriter")
    st.write("Structure structural, high-conversion visual layout blueprints for physical prints or digital canvas boards.")
    
    col1, col2 = st.columns(2)
    with col1:
        flyer_goal = st.text_input("Campaign Goal / Event Title", placeholder="e.g., Grand Opening Celebration, Charity Drive", key="t3_goal")
        offer_details = st.text_area("Value Proposition & Core Offers", placeholder="e.g., Free consultation, Buy 1 Get 1 Free, Date: Saturday 10 AM", key="t3_det")
        
        generate_flyer = st.button("Generate Layout Typography Blueprint", key="btn_flyer")
        
    with col2:
        st.subheader("Visual Hierarchy Copy Framework")
        if generate_flyer and flyer_goal:
            with st.spinner("Applying visual hierarchy text logic..."):
                prompt = f"""
                Act as an elite advertising art director and seasoned copywriter.
                Design a structured visual copy blueprint for a marketing flyer.
                Goal: {flyer_goal}
                Campaign Data Points: {offer_details}
                
                Organize the text output cleanly into explicit typographic design layers so a business owner can easily paste them into Canva or Adobe Express:
                - VISUAL ANCHOR HEADER: (The single biggest hook - short, dominant font size)
                - SUBHEADER: (The distinct value proposition or psychological trigger)
                - CORE BULLET POINTS: (Structured, concise information layout mapping time/date/offers)
                - FOOTER CALL TO ACTION (CTA): (Explicit directional instruction, e.g., 'Scan this QR code', 'Visit us at...')
                """
                output_text, routing_info = run_safely_with_fallback(prompt)
                
                if output_text:
                    st.success(f"Layout Design Architecture Formatted ({routing_info})")
                    st.write(output_text)
                else:
                    st.error("❌ High-demand infrastructure block encountered.")
                    st.warning("Google's public free-tier endpoints are fully occupied. Please retry in 30 seconds.")
