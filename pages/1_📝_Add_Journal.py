import streamlit as st
from datetime import datetime
from database.crud import create_journal
from ml.analyzer import analyze_text

st.title("📝 Add New Journal Entry")

with st.form("journal_form"):
    date = st.date_input("Date", datetime.now())
    title = st.text_input("Title (optional)")
    content = st.text_area("Write your thoughts...", height=300)
    
    submitted = st.form_submit_button("Save & Analyze")
    
    if submitted:
        if content.strip():
            # Analyze mental health
            with st.spinner("Analyzing your entry..."):
                analysis = analyze_text(content)
            
            # Save to database
            journal_id = create_journal(
                user_id=st.session_state.user_id,
                date=date,
                title=title,
                content=content,
                depression_score=analysis['score'],
                risk_level=analysis['risk_level']
            )
            
            st.success("✅ Journal entry saved!")
            st.info(f"Risk Level: {analysis['risk_level']}")
        else:
            st.error("Please write something!")