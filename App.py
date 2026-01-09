import streamlit as st
from utils.auth import check_authentication
from database.database import init_db
from database.crud import get_user_stats

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

st.info("💡 **Demo Mode**: Login with username: `demo` and password: `demo`")

# Quick stats
stats = get_user_stats(st.session_state.user_id)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Entries", stats['total_entries'])
with col2:
    st.metric("Current Streak", f"{stats['current_streak']} days")
with col3:
    st.metric("Average Risk", stats['average_risk'])

st.divider()

# Quick actions
st.subheader("Quick Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝 Write New Entry", use_container_width=True):
        st.switch_page("pages/1_📝_Add_Journal.py")

with col2:
    if st.button("📚 View All Journals", use_container_width=True):
        st.switch_page("pages/2_📚_My_Journals.py")

with col3:
    if st.button("📊 View Analytics", use_container_width=True):
        st.switch_page("pages/3_📊_Analytics.py")

st.divider()

# Information
st.subheader("How It Works")
st.markdown("""
1. **Write** your daily thoughts and feelings
2. **Analyze** - Our AI assesses your mental health patterns
3. **Track** - Monitor your emotional well-being over time
4. **Support** - Get resources and insights

**Note**: This tool is for self-awareness only and is not a substitute for professional mental health care.
""")