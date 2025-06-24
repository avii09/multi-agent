import streamlit as st
import requests

# Backend URL
API_BASE = "http://localhost:8000"


st.set_page_config(page_title="Fitness Dashboard", layout="centered")


st.markdown("<h1 style='text-align: center;'>🏋️ Fitness Studio Assistant Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### Enter your query:")


col1, col2 = st.columns([4, 1])
with col1:
    user_query = st.text_input(" ", placeholder="e.g., Show upcoming classes this week")
with col2:
    agent_choice = st.selectbox("Select Agent", ["Support Agent", "Dashboard Agent"])


session_id = None
with st.expander("⚙️ Advanced Options"):
    session_id = st.text_input("Session ID (optional)", placeholder="Enable memory by entering an ID")


def display_response(response_data):
    st.markdown("### 🤖 Agent Response")
    raw = (
        response_data.get("raw")
        or response_data.get("response", {}).get("raw")
        or response_data.get("response", {}).get("tasks_output", [{}])[0].get("raw")
        or "No response available."
    )
    st.markdown(f"**{raw}**")


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
                display_response(result.get("response", {}))
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")
