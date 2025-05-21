import os
os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"  # or use "none"

import streamlit as st
import pandas as pd
from datetime import datetime
import csv
from io import StringIO
from dataset import retrieve_data
from agent2 import agent_response

st.set_page_config(page_title="CampusCart | Shop Smart, Study Smart", layout="wide")

st.title("🛒 CampusCart - Your Smart Shopping Assistant")

# --- Product Search Section ---
st.header("🔍 Product Finder")
search_query = st.text_input("🎯 Find the Perfect Product", placeholder="e.g. noise cancelling headphones")

if search_query:
    with st.spinner("🔎 Finding the best matches for you..."):
        results = retrieve_data(search_query)
        st.subheader("📦 Top Matching Products")
        for _, row in results.iterrows():
            with st.container():
                st.markdown(f"**{row['title']}**")
                st.write(row['description'][:150] + "...")
                st.markdown(f"💰 **Price:** ${row['price']} &nbsp;&nbsp; ⭐ **Rating:** {row['average_rating']}")
                st.markdown("---")

# --- Chat Assistant Section ---
st.header("🤖 AI Chat Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chat_input = st.text_input("💬 Need help with anything?", key="chat_input", placeholder="e.g. How can I return a product?")

if chat_input:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chat_history.append(("You", chat_input, timestamp))

    with st.spinner("🤔 Thinking hard to find the best answer for you..."):
        try:
            response = agent_response(chat_input)
            if not response:
                response = "⚠️ Agent did not return a response."
            st.session_state.chat_history.append(("Agent", response, timestamp))
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            st.session_state.chat_history.append(("Agent", error_msg, timestamp))
            st.error(error_msg)

if st.session_state.chat_history:
    st.subheader("📜 Chat History")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        clear = st.button("🧹 Clear Session History")
        if clear:
            st.session_state.chat_history = []
            st.experimental_rerun()

    with col3:
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Speaker", "Message", "Timestamp"])
        writer.writerows(st.session_state.chat_history)
        st.download_button(
            label="📥 Download Chat History (CSV)",
            data=csv_buffer.getvalue(),
            file_name="chat_history.csv",
            mime="text/csv"
        )

    for speaker, message, timestamp in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"**🧑 You ({timestamp}):** {message}")
        else:
            st.markdown(f"**🤖 Agent ({timestamp}):** {message}")

# Removed SQLite and DB deletion button from sidebar as well
