import streamlit as st

def check_authentication():
    """Handle user authentication"""
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("🧠 Mental Health Journal - Login")
        
        # Show login form
        with st.form("login_form"):
            st.markdown("### Please Login")
            username = st.text_input("Username", placeholder="demo")
            password = st.text_input("Password", type="password", placeholder="demo")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                # Demo credentials
                if username == "demo" and password == "demo":
                    st.session_state.authenticated = True
                    st.session_state.user_id = 1
                    st.session_state.username = username
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Try username: demo, password: demo")
        
        st.info("💡 **Demo Credentials**: username=`demo`, password=`demo`")
        return False
    
    # Show logout button in sidebar
    with st.sidebar:
        st.write(f"👤 Logged in as: **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    return True