import streamlit as st
from openai import OpenAI
import os

# Initialize client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="SAP T-Code Explainer")

st.title("SAP T-Code Explainer")

tcode = st.text_input("Enter SAP T-Code (e.g., VA01)")

if st.button("Explain"):
    if tcode:
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

                output = response.choices[0].message.content

                st.success("Result:")
                st.write(output)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a T-Code")
