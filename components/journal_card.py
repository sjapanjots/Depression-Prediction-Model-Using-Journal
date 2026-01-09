import streamlit as st
from utils.helper import get_risk_color, truncate_text

def display_journal_card(journal):
    """Display a journal entry as a card"""
    
    risk_color = get_risk_color(journal.risk_level)
    
    # Create a card-like container
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"### {journal.title or 'Untitled Entry'}")
            st.caption(f"📅 {journal.date}")
            st.write(truncate_text(journal.content, 150))
        
        with col2:
            st.markdown(f"""
                <div style="
                    background-color: {risk_color};
                    color: white;
                    padding: 8px;
                    border-radius: 8px;
                    text-align: center;
                    font-weight: bold;
                    margin-top: 20px;
                ">
                    {journal.risk_level}
                </div>
            """, unsafe_allow_html=True)
        
        if st.button(f"📖 View Details", key=f"view_{journal.id}"):
            st.session_state.selected_journal_id = journal.id
            st.session_state.show_detail = True
        
        st.divider()