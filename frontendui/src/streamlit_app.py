import streamlit as st
from time import sleep
from navigation import make_sidebar
from utils import const_variable as cv
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)



st.header(cv.project_title, divider=cv.header_color)
make_sidebar()

st.title("Application Description")
st.write(cv.app_description)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)




# if not st.session_state["authentication_status"]:
authenticator.login()


if st.session_state["authentication_status"]:
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Dashboard')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button(cv.page1_title, type="secondary"):
            st.switch_page(cv.page1_address)
        # st.page_link("pages/page1.py", label=cv.page1_title, icon=cv.page1_icon)
    with col2:
        if st.button(cv.page2_title, type="secondary"):
            st.switch_page(cv.page2_address)        
        # st.page_link("pages/page2.py", label=cv.page2_title, icon=cv.page2_icon)
    with col3:
        if st.button(cv.page3_title, type="secondary"):
            st.switch_page(cv.page3_address)
    with col4:
        authenticator.logout()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

    st.write("Not a member yet? Sign up now!")
    if st.button("Sign up", type="secondary"):
        st.switch_page("pages/register.py")





# st.title("Log in!")
# st.write("Please log in to continue.")

# username = st.text_input("Username")
# password = st.text_input("Password", type="password")

# if st.button("Log in", type="primary"):
#     if username == "test" and password == "test":
#         st.session_state.logged_in = True
#         st.success("Logged in successfully!")
#         sleep(0.5)
#         st.switch_page("pages/page1.py")
#     else:
#         st.error("Incorrect username or password")
