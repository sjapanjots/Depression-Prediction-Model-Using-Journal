import streamlit as st
from database.crud import get_user_journals
from components.journal_card import display_journal_card

st.title("📚 My Journal Entries")

# Filters
col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input("🔍 Search journals", "")
with col2:
    sort_by = st.selectbox("Sort by", ["Newest", "Oldest", "Risk Level"])

# Get journals
journals = get_user_journals(st.session_state.user_id, search, sort_by)

if journals:
    # Display in grid
    for i in range(0, len(journals), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(journals):
                with col:
                    display_journal_card(journals[i + j])
else:
    st.info("No journal entries yet. Start writing!")
    