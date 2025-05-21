import os
os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"  # or use "none"

import streamlit as st
import pandas as pd
from dataset import retrieve_data
from agent2 import agent_response

st.set_page_config(page_title="CampusCart  Shop Smart, Study Smart", layout="wide")

st.title("Your Smart Shopping Assistant")

col1, col2 = st.columns([1.3, 2.7])

with col1:
    st.header("### 🔍 Product Finder")
    search_query = st.text_input("🎯 Find the Perfect Product", placeholder="e.g. ")

    if search_query:
        with st.spinner("Finding the best matches for you..."):
            results = retrieve_data(search_query)
            st.subheader("🔎 Top Matching Products")
            for _, row in results.iterrows():
                with st.container():
                    st.markdown(f"**{row['title']}**")
                    st.write(row['description'][:150] + "...")
                    st.markdown(f"💰 **Price:** ${row['price']} &nbsp;&nbsp; ⭐ **Rating:** {row['average_rating']}")
                    st.markdown("---")

with col2:
    st.header("🤖AI Chat Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_input = st.text_input("💬 Need help with anything?:", key="chat_input", placeholder="e.g. How can I return a product?")

    if chat_input:
        st.session_state.chat_history.append(("You", chat_input))

        # Call the agent and handle response/errors
        with st.spinner("🤔 Thinking hard to find the best answer for you..."):
            try:
                response = agent_response(chat_input)

                if not response:
                    response = "⚠️ Agent did not return a response."

                st.session_state.chat_history.append(("Agent", response))

            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.session_state.chat_history.append(("Agent", error_msg))
                st.error(error_msg)

    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"**🧑 You:** {message}")
        else:
            st.markdown(f"**🤖 Agent:** {message}")
