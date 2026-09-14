import streamlit as st
from google import genai

# 1. Page Configuration & UI Styling
st.set_page_config(
    page_title="AI Local Business Growth Suite",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI-Powered Local Business Growth Suite")
st.caption("Empowering local shops, freelancers, and small businesses with premium marketing tools.")

# GLOBAL MODEL DEFINITION (Using the universally available 1.5-flash tier)
AVAILABLE_MODEL = 'gemini-1.5-flash'

# 2. Automated Secrets Management
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
else:
    st.sidebar.header("🔑 Authentication")
    api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
    st.sidebar.markdown("💡 *Get a free key from [Google AI Studio](https://google.com)*")
    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        st.info("← Please enter your Gemini API Key in the sidebar or configure Streamlit Secrets to start.")
        st.stop()

# 3. Create Dashboard Tabs
tab1, tab2, tab3 = st.tabs([
    "💬 Review Reply Assistant", 
    "🔍 Local SEO Bundle", 
    "📢 Smart Flyer Designer"
])

# ==========================================
# TAB 1: REVIEW REPLY ASSISTANT
# ==========================================
with tab1:
    st.header("💬 Review Reply Assistant")
    st.write("Turn online reviews into professional, brand-building responses.")
    
    col1, col2 = st.columns(2)
    with col1:
        biz_name = st.text_input("Business Name", placeholder="e.g., Downtown Cafe")
        rating = st.selectbox("Star Rating Received", ["⭐⭐⭐⭐⭐ (5 Stars)", "⭐⭐⭐⭐ (4 Stars)", "⭐⭐⭐ (3 Stars)", "⭐⭐ (2 Stars)", "⭐ (1 Star)"])
        review_text = st.text_area("Paste the Customer's Review here:")
        tone = st.selectbox("Response Tone", ["Professional & Grateful", "Apologetic & Solution-Oriented", "Friendly & Casual"])
        
        generate_reply = st.button("Generate Response", key="btn_reply")
        
    with col2:
        st.subheader("Generated Response")
        if generate_reply and review_text:
            with st.spinner("Writing reply..."):
                prompt = f"""
                You are a professional PR and customer success manager for a business named '{biz_name}'.
                Write a response to a customer who left a {rating} review. 
                The customer said: "{review_text}"
                Adopt a '{tone}' tone. If the review is negative (3 stars or fewer), offer a polite way for them to contact management privately to resolve it. Do not use placeholders; make it ready to copy and paste.
                """
                response = client.models.generate_content(
                    model=AVAILABLE_MODEL,
                    contents=prompt
                )
                st.success("Done!")
                st.write(response.text)

# ==========================================
# TAB 2: LOCAL SEO BUNDLE GENERATOR
# ==========================================
with tab2:
    st.header("🔍 Local SEO Bundle Generator")
    st.write("Generate highly optimized Google Business updates and local keywords.")
    
    col1, col2 = st.columns(2)
    with col1:
        biz_type = st.text_input("Business Type / Industry", placeholder="e.g., Plumbing, Bakery, Yoga Studio")
        city_location = st.text_input("Target City / Neighborhood", placeholder="e.g., Brooklyn, NY")
        seo_topic = st.text_input("What is your update about?", placeholder="e.g., Summer discount, new menu items, weekend hours")
        
        generate_seo = st.button("Generate SEO Bundle", key="btn_seo")
        
    with col2:
        st.subheader("Your SEO Bundle")
        if generate_seo and biz_type and city_location:
            with st.spinner("Optimizing for local search..."):
                prompt = f"""
                Act as an elite Local SEO marketing expert. 
                Create a Local SEO optimization bundle for a '{biz_type}' located in '{city_location}'.
                They want to post a Google Business update about: '{seo_topic}'.
                
                Provide two sections:
                1. A high-converting, keyword-rich Google Business Profile Update post (under 1500 characters) including local call-to-actions.
                2. A list of 10 hyper-local target keywords they should include on their website meta-tags to rank #1 in '{city_location}'.
                """
                response = client.models.generate_content(
                    model=AVAILABLE_MODEL,
                    contents=prompt
                )
                st.success("Done!")
                st.write(response.text)

# ==========================================
# TAB 3: SMART FLYER DESIGNER
# ==========================================
with tab3:
    st.header("📢 Smart Flyer Designer")
    st.write("Get beautifully structured, high-conversion copy for physical flyers or social media graphics.")
    
    col1, col2 = st.columns(2)
    with col1:
        flyer_goal = st.text_input("Flyer Goal / Event Name", placeholder="e.g., Grand Opening, Holiday Sale, Charity Drive")
        offer_details = st.text_area("Key Details & Offers", placeholder="e.g., 20% off all items, Free coffee for first 50 people, Saturday 10 AM - 4 PM")
        
        generate_flyer = st.button("Structure Flyer Copy", key="btn_flyer")
        
    with col2:
        st.subheader("Visual Text Hierarchy Blueprint")
        if generate_flyer and flyer_goal:
            with st.spinner("Designing copy layout..."):
                prompt = f"""
                Act as a professional graphic designer and advertising copywriter.
                Create a high-impact, visual text blueprint for a marketing flyer.
                Goal: {flyer_goal}
                Details to include: {offer_details}
                
                Structure the output visually as text sections that a user can easily copy into Canva or Adobe Express:
                - HEADER (The big hook - short and catchy)
                - SUBHEADER (The value proposition)
                - BODY COPY / BULLET POINTS (Key event details or offers)
                - CALL TO ACTION (What to do next, e.g., 'Scan this QR code', 'Visit us at...')
                """
                response = client.models.generate_content(
                    model=AVAILABLE_MODEL,
                    contents=prompt
                )
                st.success("Done!")
                st.write(response.text)
