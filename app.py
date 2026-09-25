import streamlit as st
from google import genai
from google.genai import types
import os

st.set_page_config(page_title="Local Business Suite", page_icon="🏢", layout="wide")

# Ensure API Key
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

st.title("🏢 Local Business Suite - Enterprise AI Platform")

# Top Navigation Tabs
tab_franchise, tab_wa, tab_reviews, tab_seo, tab_transcribe = st.tabs([
    "🏢 Franchise Hub",
    "💬 WhatsApp Formatter",
    "⭐ Review Responder",
    "📍 Local SEO",
    "🎙️ Audio Transcriber"
])

# ----------------- 1. FRANCHISE HUB -----------------
with tab_franchise:
    st.subheader("Multi-Location Franchise Command")
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Store Branches", "4 Locations", "100% Live")
    col2.metric("Network Health Index", "95.2%", "+2.4%")
    col3.metric("Customer Ingestion Volume", "1,126 reviews/mo", "Healthy")
    
    st.selectbox("Select Active Working Branch:", [
        "Austin Flagship Bakery & Cafe (Austin, TX)",
        "Downtown Manhattan Espresso Bar (New York, NY)",
        "London Covent Garden Patisserie (London, UK)",
        "Mumbai Bandra West Cafe & Bistro (Mumbai, India)"
    ])

# ----------------- 2. WHATSAPP FORMATTER -----------------
with tab_wa:
    st.subheader("WhatsApp Business Message Formatter")
    c1, c2 = st.columns(2)
    with c1:
        wa_name = st.text_input("Customer Name", value="John M.")
        wa_goal = st.selectbox("Objective", [
            "Order Dispatched / Ready for Pickup",
            "Appointment / Booking Confirmation",
            "Weekend Flash Sale & Discount",
            "5-Star Google Review Request"
        ])
        wa_details = st.text_area("Order / Offer Details", value="Order #8291 of sourdough loaves is ready for pickup.")
        wa_cta = st.text_input("Call to Action", value="Reply 1 to confirm pickup, or call 555-0192.")
        
        output = None  # Prevents NameError!
        if st.button("Format for WhatsApp 💬", type="primary"):
            if client:
                with st.spinner("Drafting WhatsApp Message..."):
                    try:
                        res = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=f"Business: Artisan Bakery\nCustomer: {wa_name}\nGoal: {wa_goal}\nDetails: {wa_details}\nCTA: {wa_cta}\n\nFormat as a polished WhatsApp chat with *bold*, _italics_, and emojis.",
                        )
                        output = res.text
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please configure GEMINI_API_KEY in your Streamlit secrets.")
    
    with c2:
        if output:
            st.success("WhatsApp Ready Copy:")
            st.code(output, language="markdown")

# ----------------- 3. REVIEW RESPONDER -----------------
with tab_reviews:
    st.subheader("Google & Yelp Review Responder")
    rev_author = st.text_input("Reviewer Name", value="Sarah K.")
    rev_rating = st.slider("Rating (Stars)", 1, 5, 5)
    rev_text = st.text_area("Review Text", value="Loved the warm cinnamon rolls and espresso! Friendly baristas.")
    if st.button("Generate Public Response ⭐"):
        if client:
            with st.spinner("Drafting response..."):
                res = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"Write a warm, brand-building review response to {rev_author} who left a {rev_rating}-star review: '{rev_text}'"
                )
                st.write(res.text)

# ----------------- 4. LOCAL SEO -----------------
with tab_seo:
    st.subheader("Local SEO & Google Maps Optimizer")
    city = st.text_input("Target City / Area", value="Austin, TX")
    category = st.text_input("Category", value="Artisanal Bakery & Specialty Coffee")
    if st.button("Generate Local Keywords & Google Description 📍"):
        if client:
            with st.spinner("Optimizing local SEO..."):
                res = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"Generate top 10 high-intent local keywords and a 700-char Google Business Profile description for a {category} in {city}."
                )
                st.write(res.text)

# ----------------- 5. AUDIO TRANSCRIBER -----------------
with tab_transcribe:
    st.subheader("Audio Transcription (Gemini 3.5 Transcribe)")
    audio_file = st.file_uploader("Upload Audio Memo (.wav, .mp3, .m4a)", type=["wav", "mp3", "m4a"])
    if audio_file and st.button("Transcribe Audio 🎙️"):
        st.info("Audio uploaded. Processing through Gemini...")
