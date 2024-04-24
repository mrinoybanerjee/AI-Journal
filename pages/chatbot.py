import streamlit as st
from src.logic import handle_query

def show():
    st.title("Interact with Penpal ✨")
    
    with st.form("Chatbot Form"):
        user_query = st.text_input("Ask Penpal:", placeholder="Type your message here...")
        submitted = st.form_submit_button("Send Query")
        if submitted:
            st.write("Penpal is thinking ✨, please hold on for a moment...")
            response = handle_query(user_query)
            st.write("Journal Bot:", response)
