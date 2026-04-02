import streamlit as st
from openai import OpenAI
import os

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="SAP T-Code Explainer", layout="wide")

# ---------------- SESSION STATE ----------------
if "output" not in st.session_state:
    st.session_state.output = ""
if "tcode" not in st.session_state:
    st.session_state.tcode = ""
if "usage" not in st.session_state:
    st.session_state.usage = {}

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align: center;'>SAP T-Code Explainer</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- LAYOUT ----------------
left, right = st.columns([2, 1])

# ---------------- LEFT SIDE ----------------
with left:
    st.subheader("🔍 Input")

    tcode = st.text_input(
        "Enter SAP T-Code (e.g., VA01)",
        Key="tcode"
    )

    col1, col2 = st.columns([1, 1])

    # -------- EXPLAIN BUTTON --------
    with col1:
        if st.button("Explain"):
            if tcode:
                st.session_state.tcode = tcode

                with st.spinner("Fetching details..."):
                    prompt = f"""
                    Explain the SAP transaction code {tcode} in 2 concise points:
                    1. Purpose
                    2. Whether it is transactional or not (Yes/No)
                    Keep it very short and clear.
                    """

                    try:
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": prompt}]
                        )

                        st.session_state.output = response.choices[0].message.content
                        st.session_state.usage = response.usage

                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter a T-Code")

    # -------- RESET BUTTON --------
    with col2:
        if st.button("Reset"):
            st.session_state.tcode = ""
            st.session_state.output = ""
            st.session_state.usage = {}
            st.rerun()

    # -------- OUTPUT --------
    if st.session_state.output:
        st.markdown("### ✅ Result")
        st.success(st.session_state.output)

# ---------------- RIGHT SIDE ----------------
with right:
    st.subheader("📊 Token Usage & Cost")

    usage = st.session_state.usage

    if usage:
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens

        # Approx pricing (gpt-4o-mini)
        cost_per_1k_tokens_usd = 0.00015
        cost_usd = (total_tokens / 1000) * cost_per_1k_tokens_usd
        cost_inr = cost_usd * 83  # approx conversion

        st.metric("Input Tokens", input_tokens)
        st.metric("Output Tokens", output_tokens)
        st.metric("Total Tokens", total_tokens)

        st.markdown("---")
        st.metric("Cost (USD)", f"${cost_usd:.6f}")
        st.metric("Cost (INR)", f"₹{cost_inr:.4f}")

    else:
        st.info("Run a query to see usage")

    st.markdown("---")

    st.markdown("### ℹ️ What is a token?")
    st.write("""
    - Tokens are pieces of words used by AI models  
    - 1 token ≈ 3–4 characters  
    - Both input and output consume tokens  
    - Pricing is based on total tokens processed  
    """)
