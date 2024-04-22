import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from utils import const_variable as cv

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title(cv.side_bar_title)
        st.write("")
        st.write("")
        st.page_link("streamlit_app.py", label='home', icon='🏠')

        if st.session_state.get('authentication_status', False):
            st.page_link(cv.page1_address, label=cv.page1_title, icon=cv.page1_icon)
            st.page_link(cv.page2_address, label=cv.page2_title, icon=cv.page2_icon)
            st.page_link(cv.page3_address, label=cv.page3_title, icon=cv.page3_icon)


            st.write("")
            st.write("")

            # if st.button("Log out"):
            #     logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")

def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("streamlit_app.py")
