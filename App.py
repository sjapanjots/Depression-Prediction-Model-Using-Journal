import streamlit as st
from utils.auth import check_authentication
from database.database import init_db

# Page config
st.set_page_config(
    page_title="Mental Health Journal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Authentication
if not check_authentication():
    st.stop()

# Home page
st.title("🧠 Mental Health Journal")
st.markdown("Welcome to your personal mental health journaling space.")

# Quick stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Entries", "24")
with col2:
    st.metric("Current Streak", "7 days")
with col3:
    st.metric("Average Risk", "Low")

# Recent journals preview
st.subheader("Recent Entries")
# Display recent journal cards