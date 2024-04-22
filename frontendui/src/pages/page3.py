from navigation import make_sidebar
import streamlit as st
import requests
from utils import const_variable as cv
import pandas as pd

st.header(cv.project_title, divider=cv.header_color)
make_sidebar()

st.write(
    f"""
# {cv.page3_title}

{cv.page3_description}
"""
)