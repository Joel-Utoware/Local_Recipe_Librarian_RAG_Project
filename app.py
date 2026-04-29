# app.py

import streamlit as st
from rag_pipeline import generate_answer


# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Local Recipe Librarian",
    page_icon="🍳",
    layout="centered"
)

# -------------------------
# Title
# -------------------------
st.title("🍳 Local Recipe Librarian")
st.caption("Ask questions about recipes using your local RAG assistant.")

# -------------------------
# Session State
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Input Form
# -------------------------
with st.form("query_form"):
    user_query = st.text_input(
        "What would you like to cook?",
        placeholder="Example: easy spicy chicken dinner"
    )

    submitted = st.form_submit_button("Search")

# -------------------------
# Run Query
# -------------------------
if submitted:

    if user_query.strip():

        with st.spinner("Searching recipes and generating answer..."):
            response = generate_answer(user_query)

        # Save history
        st.session_state.history.append(
            {
                "query": user_query,
                "response": response
            }
        )

    else:
        st.warning("Please enter a recipe question.")

# -------------------------
# Show Latest Result
# -------------------------
if st.session_state.history:

    latest = st.session_state.history[-1]

    st.subheader("📌 Latest Answer")
    st.write(latest["response"])

# -------------------------
# Search History
# -------------------------
if st.session_state.history:

    with st.expander("🕘 Previous Searches"):

        for item in reversed(st.session_state.history[:-1]):

            st.markdown(f"**Question:** {item['query']}")
            st.write(item["response"])
            st.divider()