from navigation import make_sidebar
import streamlit as st
from utils import const_variable as cv

st.header(cv.project_title, divider=cv.header_color)
make_sidebar()

st.write(
    f"""
# {cv.page1_title}

In this page we will analyze the carbon emissions of a company. We will look at the carbon emissions of the company in different regions and compare them to the company's carbon emissions goals. We will also look at the company's carbon emissions over time and see how they have changed.

"""
)
