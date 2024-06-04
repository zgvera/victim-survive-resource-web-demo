import streamlit as st
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
from streamlit_option_menu import option_menu # pip install streamlit_option_menu
import sqlite3
import openai  # pip install openai

# Set your OpenAI API key from Streamlit secrets
# openai.api_key = st.secrets["openai_api_key"]

client = openai.OpenAI(api_key = st.secrets["openai_api_key"])

# Set page configuration
st.set_page_config(
    page_title="Victim Resource Documentation Center",
    page_icon="✅",
    layout="wide",
)

# Create a sqlite database to store user information.
conn = sqlite3.connect('dat.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT, password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO usertable(username, password) VALUES (?,?)', (username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM usertable WHERE username=? AND password=?', (username, password))
    data = c.fetchall()
    return data

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False

def main():
    def show_chatbox():
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        user_query = st.text_input("You:", key="user_query")
        if st.button("Send"):
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
            if st.session_state.chat_history:
                messages += st.session_state.chat_history
            messages.append({"role": "user", "content": user_query})

            response = client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            st.session_state.chat_history.append({"role": "user", "content": user_query})
            st.session_state.chat_history.append({"role": "assistant", "content": response.choices[0].message["content"]})
            st.experimental_rerun()  # Refresh the chatbox to show new messages

        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.write(f"**You**: {message['content']}")
                else:
                    st.write(f"**Bot**: {message['content']}")

    if st.session_state.logged_in:
        # User is logged in
        with st.sidebar:
            selected_page = option_menu(
                menu_title="Navigation",
                options=["What should I do now?", "Profile", "Documentation", "Resources"],
                icons=['question-circle', 'person', 'file-text', 'info'],
                menu_icon="cast",
                default_index=0
            )

        # Common chat button
        if st.button("Chat", key="chat_button"):
            st.session_state.show_chat = not st.session_state.show_chat

        if st.session_state.show_chat:
            show_chatbox()

        # Page content based on selection
        if selected_page == "What should I do now?":
            st.title("What should I do now?")
            st.write("""
            If you are facing sexual violence, it is important to seek help and support. Here are some steps you can take:
            1. Reach out to a trusted friend or family member.
            2. Contact a local support organization or hotline.
            3. Consider reporting the incident to the authorities.
            4. Seek medical attention if necessary.
            5. Take care of yourself and prioritize your mental health.
            """)
        elif selected_page == "Profile":
            st.title("Profile")
            st.write("Profile page content")
        elif selected_page == "Documentation":
            st.title("Documentation")
            st.write("Documentation page content")
        elif selected_page == "Resources":
            st.title("Resources")
            st.write("Resources page content")

    else:
        # Show login or sign-up options
        st.title("Victim Resource Documentation Center")
        st.subheader("SignUp to get access ...")

        choice = option_menu(menu_title=None,
                             options=["Login", "SignUp"],
                             icons=['house', 'book'],
                             menu_icon="cast",
                             default_index=0)

        if choice == "Login":
            st.subheader("Login Section")
            username = st.text_input("User Name")
            password = st.text_input("Password", type='password')
            if st.button("Login"):
                create_usertable()
                result = login_user(username, password)
                if result:
                    st.session_state.logged_in = True
                    st.experimental_rerun()  # Refresh the page
                else:
                    st.error("Invalid username or password")

        elif choice == "SignUp":
            st.subheader("Register Here!")
            new_user = st.text_input("Username")
            new_password = st.text_input("Password", type='password')
            if st.button("SignUp"):
                create_usertable()
                add_userdata(new_user, new_password)
                st.success("You have successfully created a valid Account")
                st.info("Please Login...")

if __name__ == "__main__":
    main()
