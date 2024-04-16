import streamlit as st
from time import sleep
from navigation import make_sidebar
from utils import const_variable as cv

st.header(cv.project_title, divider=cv.header_color)
make_sidebar()

st.title("Application Description")
st.write(cv.app_description)

st.title("Log in!")
st.write("Please log in to continue.")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Log in", type="primary"):
    if username == "test" and password == "test":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/page1.py")
    else:
        st.error("Incorrect username or password")
