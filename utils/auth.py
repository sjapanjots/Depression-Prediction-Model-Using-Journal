import streamlit as st
import streamlit_authenticator as stauth

def check_authentication():
    """Handle user authentication"""
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        # Show login form
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                # Validate credentials (implement properly)
                if username == "demo" and password == "demo":
                    st.session_state.authenticated = True
                    st.session_state.user_id = 1
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        return False
    
    return True