import streamlit as st
import requests

# Backend URL
API_BASE = "http://localhost:8000"

# Page setup
st.set_page_config(page_title="Fitness Dashboard", layout="centered")

# Header
st.markdown("<h1 style='text-align: center;'>🏋️ Fitness Studio Assistant Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### Enter your query:")

# Input + Agent Selector side-by-side
col1, col2 = st.columns([4, 1])
with col1:
    user_query = st.text_input(" ", placeholder="e.g., Show upcoming classes this week")
with col2:
    agent_choice = st.selectbox("Select Agent", ["Support Agent", "Dashboard Agent"])

# 🔐 Optional Session ID (Memory) in Advanced Options
session_id = None
with st.expander("⚙️ Advanced Options"):
    session_id = st.text_input("Session ID (optional)", placeholder="Enable memory by entering an ID")

# Submit button
if st.button("Submit"):
    if not user_query:
        st.warning("Please enter a query.")
    else:
        endpoint = "/support/query" if agent_choice == "Support Agent" else "/dashboard/query"
        payload = {"prompt": user_query}
        if session_id:
            payload["session_id"] = session_id

        try:
            response = requests.post(f"{API_BASE}{endpoint}", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.markdown("### 🤖 Agent Response:")
                st.write(result.get("response"))
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")
