import streamlit as st
from src.logic import add_journal_entry

def show():
    st.title("Add a New Journal Entry 📝")
    
    with st.form("Journal Form"):
        user_input = st.text_area("Enter your log:", height=150, placeholder="Type here...")
        submitted = st.form_submit_button("Add Entry")
        if submitted:
            response = add_journal_entry(user_input)
            st.success("Entry added: " + response)
