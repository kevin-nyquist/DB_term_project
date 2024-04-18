from navigation import make_sidebar
import streamlit as st
import requests
from utils import const_variable as cv
import pandas as pd

st.header(cv.project_title, divider=cv.header_color)
make_sidebar()

st.write(
    f"""
# {cv.page1_title}

In this page we will analyze the carbon emissions of a company. We will look at the carbon emissions of the company in different regions and compare them to the company's carbon emissions goals. We will also look at the company's carbon emissions over time and see how they have changed.

"""
)


if st.button("Companies"):
    data = requests.get("http://service:80/companies/").json()
    st.write(pd.DataFrame(data))

c_id = st.text_input('Company ID', '1')
if st.button("Company"):
    data = requests.get(f"http://service:80/companies/{c_id}").json()
    st.write(pd.DataFrame([data]))
    
c_id2 = st.text_input('Company ID ', '1')
if st.button("branches"):
    data = requests.get(f"http://service:80/branches/{c_id2}").json()
    st.write(pd.DataFrame(data))