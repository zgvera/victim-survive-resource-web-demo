'''
This file is the homepage of the web app.
'''
import streamlit as st


# Home page inspired by https://github.com/soumenksarker/Live-Bank-Data-Dashboard

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu # pip install streamlit_option_menu
import numpy as np
import sqlite3
import time

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="Victim Resource Documentation Center",
    page_icon="✅",
    layout="wide",
)


# Create a sqlite database to store user information.

conn = sqlite3.connect('dat.db')
c=conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT,password TEXT)')
def add_userdata(username, password):
    c.execute('INSERT INTO usertable(username, password) VALUES (?,?)',(username, password))
    conn.commit()
def login_user(username, password):
    c.execute('SELECT * FROM usertable WHERE username=? AND password=?', (username, password))
    data = c.fetchall()
    return data
def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data


## log in or sign up selection

st.subheader("SignUp to get access ...")
choice = option_menu(menu_title=None,
options= ["Login","SignUp"], 
icons=['house','book'],
menu_icon="cast",
default_index=0,
#orientation="horizontal"
)

st.title("Victim Resource Documentation Center")

### Show different layouts if choose login or sign up.

if choice == "Login":
    #st.session_state.history=[]
    st.subheader("Login Section")
    username = st.text_input("User Name")
    password = st.text_input("Password", type='password')
    if st.checkbox("Login"):
        create_usertable()
        result=login_user(username, password)
        
        
elif choice == "SignUp":
    st.subheader("Register Here!")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    if st.button("SignUp"):
        create_usertable()
        add_userdata(new_user, new_password)
        st.success("You have successfully created a valid Account")
        st.info("Please Login...")

