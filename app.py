# ============================================================
# AI LOCAL BUSINESS GROWTH SUITE PRO
# Version 3.0
# ============================================================

import os
import time
import urllib.parse
from typing import Optional

import streamlit as st
from google import genai


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Local Business Growth Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. PREMIUM UI
# ============================================================

st.markdown(
    """
    <style>

    .main-header {
        font-size: 2.7rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .sub-caption {
        font-size: 1.05rem;
        opacity: 0.75;
        margin-bottom: 1.5rem;
    }

    .hero {
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid rgba(128,128,128,0.25);
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

    .small-text {
        font-size: 0.85rem;
        opacity: 0.65;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. APPLICATION CONSTANTS
# ============================================================

APP_NAME = "AI Local Business Growth Suite Pro"
APP_VERSION = "3.0"

MODEL_NAME = "gemini-2.5-flash"

APP_URL = "https://streamlit.app"


# ============================================================
# 4. SESSION STATE
# ============================================================

if "interactions" not in st.session_state:
    st.session_state.interactions = 0

if "generation_history" not in st.session_state:
    st.session_state.generation_history = []

if "business_name" not in st.session_state:
    st.session_state.business_name = ""

if "business_type" not in st.session_state:
    st.session_state.business_type = ""

if "business_location" not in st.session_state:
    st.session_state.business_location = ""

if "brand_voice" not in st.session_state:
    st.session_state.brand_voice = "Professional & Friendly"


# ============================================================
# 5. API CONFIGURATION
# ============================================================

def get_api_key() -> Optional[str]:
    """
    Read the Gemini API key securely from Streamlit secrets
    or environment variables.
    """

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
# 6. AI ENGINE
# ============================================================

class AIEngine:
    """Centralized Gemini AI service."""

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError(
                "Gemini API key was not found."
            )

        self.client = genai.Client(api_key=api_key)

    def generate(
        self,
        prompt: str,
        system_instruction: str = "",
    ) -> str:

        try:

            config = {}

            if system_instruction:
                config["system_instruction"] = system_instruction

            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=config,
            )

            if not response:
                raise RuntimeError(
                    "AI returned no response."
                )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError(
                    "AI returned an empty response."
                )

            return text.strip()

        except Exception as error:

            raise RuntimeError(
                f"AI generation failed: {error}"
            ) from error


# ============================================================
# 7. SAFE AI CALL
# ============================================================

def run_ai(
    prompt: str,
    system_instruction: str,
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

        return (
            result,
            f"⚡ Gemini {MODEL_NAME} • {elapsed:.1f}s",
        )

    except Exception as error:

        return (
            None,
            str(error),
        )


# ============================================================
# 8. HISTORY
# ============================================================

def save_history(
    feature: str,
    output: str,
):

    st.session_state.generation_history.insert(
        0,
        {
            "feature": feature,
            "output": output,
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
    )

    # Keep only recent generations
    st.session_state.generation_history = (
        st.session_state.generation_history[:20]
    )


# ============================================================
# 9. BUSINESS CONTEXT
# ============================================================

def business_context() -> str:

    return f"""
Business name: {st.session_state.business_name or "Not provided"}

Business category:
{st.session_state.business_type or "Not provided"}

Location:
{st.session_state.business_location or "Not provided"}

Brand voice:
{st.session_state.brand_voice}
"""


# ============================================================
# 10. COMMON SYSTEM INSTRUCTIONS
# ============================================================

REVIEW_SYSTEM = """
You are an expert local-business reputation manager.

Write professional, natural and helpful customer-review responses.

Never invent facts.

For negative reviews:
- remain respectful
- acknowledge the concern
- avoid arguments
- encourage appropriate private resolution

Do not make unrealistic promises.
"""

SEO_SYSTEM = """
You are an expert local SEO strategist.

Create useful local-business content.

Avoid keyword stuffing.
Avoid fake claims.
Use natural language.
Focus on customer usefulness, local relevance and clear calls to action.
"""

FLYER_SYSTEM = """
You are a professional advertising and flyer copywriter.

Create clear promotional copy with strong hierarchy.

Use:
HEADLINE
SUBHEADLINE
KEY BENEFITS
OFFER
CALL TO ACTION

Do not invent prices, addresses or offers that were not provided.
"""

WHATSAPP_SYSTEM = """
You are an expert WhatsApp marketing copywriter.

Create concise, friendly promotional messages.

Use WhatsApp-compatible formatting such as:
*bold text*

Use emojis where appropriate.

Never create misleading claims or fake urgency.
"""

LOCALIZATION_SYSTEM = """
You are an expert Indian regional-language marketing copywriter.

Translate and culturally localize the content naturally.

Do not perform awkward word-for-word translation.

Preserve the original business meaning.
"""


# ============================================================
# 11. HEADER
# ============================================================

st.markdown(
    '<div class="main-header">🚀 AI Local Business Growth Suite Pro</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sub-caption">'
    "One intelligent workspace for local-business marketing, content and growth."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# 12. SIDEBAR
# ============================================================

with st.sidebar:

    st.title("💎 Business Dashboard")

    st.markdown("### 🏪 Business Profile")

    st.session_state.business_name = st.text_input(
        "Business Name",
        value=st.session_state.business_name,
        placeholder="Shiva Bakery",
    )

    st.session_state.business_type = st.text_input(
        "Business Category",
        value=st.session_state.business_type,
        placeholder="Bakery",
    )

    st.session_state.business_location = st.text_input(
        "Business Location",
        value=st.session_state.business_location,
        placeholder="Kalaburagi, Karnataka",
    )

    st.session_state.brand_voice = st.selectbox(
        "Brand Voice",
        [
            "Professional & Friendly",
            "Premium & Elegant",
            "Simple & Local",
            "Energetic & Youthful",
            "Warm & Family-Friendly",
        ],
    )

    st.divider()

    st.metric(
        "AI Generations",
        st.session_state.interactions,
    )

    st.metric(
        "Saved Results",
        len(st.session_state.generation_history),
    )

    st.divider()

    if API_KEY:
        st.success("🟢 AI Engine Ready")
    else:
        st.warning("🟡 API Key Required")

    st.caption(
        f"{APP_NAME} v{APP_VERSION}"
    )


# ============================================================
# 13. API KEY WARNING
# ============================================================

if not API_KEY:

    st.info(
        """
        🔐 **AI engine is waiting for configuration.**

        Add your Gemini API key to:

        `.streamlit/secrets.toml`

        Example:

        `GEMINI_API_KEY = "YOUR_KEY"`
        """
    )


# ============================================================
# 14. DASHBOARD METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "🤖 AI Engine",
        "Ready" if API_KEY else "Setup",
    )

with m2:
    st.metric(
        "📊 Generations",
        st.session_state.interactions,
    )

with m3:
    st.metric(
        "💾 History",
        len(st.session_state.generation_history),
    )

with m4:
    st.metric(
        "🌐 Languages",
        "4+",
    )


st.divider()


# ============================================================
# 15. MAIN TABS
# ============================================================

tabs = st.tabs(
    [
        "💬 Reviews",
        "🔍 Local SEO",
        "📢 Flyer",
        "📱 WhatsApp",
        "🌐 Regional",
        "📅 Campaign",
        "🕘 History",
    ]
)


# ============================================================
# TAB 1 — REVIEW ASSISTANT
# ============================================================

with tabs[0]:

    st.header("💬 AI Review Assistant")

    left, right = st.columns(2)

    with left:

        review_rating = st.selectbox(
            "Customer Rating",
            [
                "5 Stars",
                "4 Stars",
                "3 Stars",
                "2 Stars",
                "1 Star",
            ],
        )

        review_text = st.text_area(
            "Customer Review",
            height=180,
            placeholder="Paste the customer review here...",
        )

        review_tone = st.selectbox(
            "Response Style",
            [
                "Professional & Grateful",
                "Warm & Friendly",
                "Apologetic & Solution-Oriented",
            ],
        )

        generate_review = st.button(
            "✨ Generate Review Response",
            use_container_width=True,
        )

    with right:

        st.subheader("Optimized Response")

        if generate_review:

            if not review_text.strip():

                st.warning(
                    "Please enter a customer review."
                )

            elif not st.session_state.business_name:

                st.warning(
                    "Please enter your business name in the sidebar."
                )

            else:

                prompt = f"""
{business_context()}

Customer rating:
{review_rating}

Customer review:
{review_text}

Response style:
{review_tone}

Write one polished public response.
"""

                with st.spinner(
                    "Analyzing customer feedback..."
                ):

                    output, trace = run_ai(
                        prompt,
                        REVIEW_SYSTEM,
                    )

                if output:

                    save_history(
                        "Review Assistant",
                        output,
                    )

                    st.success(trace)

                    st.markdown(
                        '<div class="output-box">',
                        unsafe_allow_html=True,
                    )

                    st.write(output)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True,
                    )

                    st.download_button(
                        "⬇️ Download Response",
                        output,
                        file_name="review_response.txt",
                        mime="text/plain",
                    )

                else:

                    st.error(trace)


# ============================================================
# TAB 2 — SEO
# ============================================================

with tabs[1]:

    st.header("🔍 Local SEO Optimizer")

    left, right = st.columns(2)

    with left:

        seo_topic = st.text_input(
            "Campaign / Topic",
            placeholder="Festival season promotion",
        )

        seo_keywords = st.text_input(
            "Important Keywords",
            placeholder="bakery, cakes, birthday cakes",
        )

        generate_seo = st.button(
            "🚀 Generate SEO Package",
            use_container_width=True,
        )

    with right:

        st.subheader(
            "SEO Growth Package"
        )

        if generate_seo:

            if not st.session_state.business_name:
                st.warning(
                    "Add your business name first."
                )

            elif not st.session_state.business_location:
                st.warning(
                    "Add your location first."
                )

            else:

                prompt = f"""
{business_context()}

Campaign topic:
{seo_topic}

Important keywords:
{seo_keywords}

Create a local SEO package containing:

1. Google Business Profile post
2. Local SEO description
3. 10 relevant keyword ideas
4. 5 local content ideas
5. One clear CTA

Keep everything natural and useful.
"""

                with st.spinner(
                    "Building local SEO strategy..."
                ):

                    output, trace = run_ai(
                        prompt,
                        SEO_SYSTEM,
                    )

                if output:

                    save_history(
                        "Local SEO",
                        output,
                    )

                    st.success(trace)

                    st.markdown(output)

                    st.download_button(
                        "⬇️ Download SEO Package",
                        output,
                        file_name="local_seo_package.txt",
                        mime="text/plain",
                    )

                else:

                    st.error(trace)


# ============================================================
# TAB 3 — FLYER
# ============================================================

with tabs[2]:

    st.header("📢 AI Flyer Copy Designer")

    left, right = st.columns(2)

    with left:

        flyer_goal = st.text_input(
            "Campaign Title",
            placeholder="Grand Opening",
        )

        flyer_details = st.text_area(
            "Offer / Details",
            height=160,
            placeholder="50% discount this Saturday",
        )

        flyer_cta = st.text_input(
            "Call To Action",
            placeholder="Visit us today!",
        )

        generate_flyer = st.button(
            "🎨 Generate Flyer Copy",
            use_container_width=True,
        )

    with right:

        st.subheader(
            "Professional Flyer Blueprint"
        )

        if generate_flyer:

            if not flyer_goal:
                st.warning(
                    "Enter a campaign title."
                )

            else:

                prompt = f"""
{business_context()}

Campaign:
{flyer_goal}

Details:
{flyer_details}

CTA:
{flyer_cta}

Create professional flyer copy in this structure:

HEADLINE

SUBHEADLINE

KEY BENEFITS

OFFER

CALL TO ACTION

FOOTER

Make it suitable for Canva.
"""

                with st.spinner(
                    "Designing promotional copy..."
                ):

                    output, trace = run_ai(
                        prompt,
                        FLYER_SYSTEM,
                    )

                if output:

                    save_history(
                        "Flyer Designer",
                        output,
                    )

                    st.success(trace)

                    st.markdown(output)

                    st.download_button(
                        "⬇️ Download Flyer Copy",
                        output,
                        file_name="flyer_copy.txt",
                        mime="text/plain",
                    )

                else:

                    st.error(trace)


# ============================================================
# TAB 4 — WHATSAPP
# ============================================================

with tabs[3]:

    st.header(
        "📱 WhatsApp Marketing Formatter"
    )

    left, right = st.columns(2)

    with left:

        whatsapp_input = st.text_area(
            "Your Raw Message",
            height=180,
            placeholder="Fresh mangoes available today...",
        )

        whatsapp_cta = st.text_input(
            "CTA",
            placeholder="Call 9999999999",
        )

        generate_whatsapp = st.button(
            "📲 Create WhatsApp Message",
            use_container_width=True,
        )

    with right:

        st.subheader(
            "Copy-Paste WhatsApp Message"
        )

        if generate_whatsapp:

            if not whatsapp_input.strip():

                st.warning(
                    "Enter your promotional message."
                )

            else:

                prompt = f"""
{business_context()}

Raw promotional message:
{whatsapp_input}

CTA:
{whatsapp_cta}

Create a WhatsApp broadcast message.

Use:
*bold text*

Use suitable emojis.
Keep it readable and persuasive.
"""

                with st.spinner(
                    "Creating WhatsApp campaign..."
                ):

                    output, trace = run_ai(
                        prompt,
                        WHATSAPP_SYSTEM,
                    )

                if output:

                    save_history(
                        "WhatsApp Formatter",
                        output,
                    )

                    st.success(trace)

                    st.code(
                        output,
                        language="text",
                    )

               whatsapp_url = "https://wa.me/?text=" + urllib.parse.quote(output)

        st.link_button("💬 Open WhatsApp", whatsapp_url)
