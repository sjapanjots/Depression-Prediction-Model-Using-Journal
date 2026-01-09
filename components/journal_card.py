import streamlit as st
from utils.helpers import get_risk_color

def display_journal_card(journal):
    """Display a journal entry as a card"""
    
    risk_color = get_risk_color(journal.risk_level)
    
    with st.container():
        st.markdown(f"""
        <div style="
            border: 2px solid {risk_color};
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            background-color: rgba(255,255,255,0.05);
        ">
            <h4>{journal.title or 'Untitled'}</h4>
            <p style="color: gray;">{journal.date}</p>
            <p>{journal.content[:100]}...</p>
            <span style="
                background-color: {risk_color};
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
            ">
                {journal.risk_level} Risk
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"View Full Entry", key=f"btn_{journal.id}"):
            st.session_state.selected_journal = journal.id
            st.switch_page("pages/2_📚_My_Journals.py")
            
            