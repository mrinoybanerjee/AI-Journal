import streamlit as st

# Define your pages as functions
def main():
    st.title('Pen-pal 📝')
    st.write("Pen-pal is your AI-enabled journaling app.")
    st.write('Navigate to the pages using the sidebar to add journal entries or interact with the chatbot.')

def page_journal():
    from pages import journal
    journal.show()

def page_chatbot():
    from pages import chatbot
    chatbot.show()

# Add pages to the sidebar for navigation
page_names_to_funcs = {
    "Home": main,
    "Add Journal Entry": page_journal,
    "Interact with Chatbot": page_chatbot,
}

selected_page = st.sidebar.selectbox("Select a Page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()






