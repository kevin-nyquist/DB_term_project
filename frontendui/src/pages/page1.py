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


col1, col2 = st.columns(2)

with col1:
    company = requests.get("http://service:80/companies/").json()
    company = pd.DataFrame(company)
    company_name = company["c_name"].tolist()

    sel_comp_name = st.selectbox(
        'Companies',
        company_name)
    sel_comp_id = company[company["c_name"] == sel_comp_name]["id"].values[0]

with col2:
    company_branches = requests.get(f"http://service:80/companies/{sel_comp_id}/branches").json() 
    company_branches = pd.DataFrame(company_branches)
    company_branches_name = company_branches["branch_name"].tolist()

    sel_branch_name = st.selectbox(
        'branches',
        company_branches_name)
    sel_branch_id = company_branches[company_branches["branch_name"] == sel_branch_name]["id"].values[0]


carbon_offsets = requests.get(f"http://service:80/companies/{sel_comp_id}/carbon_offsets/").json()
carbon_offsets = pd.DataFrame(carbon_offsets)

number_of_branches = len(company_branches)

st.write("## Total Information of the Company")
company_info = {"Company Name": sel_comp_name, 
                "Company ID": sel_comp_id, 
                "Total number of branches": number_of_branches}
company_info = pd.DataFrame([company_info])
st.write(f"- ### Company Info")
st.write(company_info)
st.write("- ### Company Branches")
st.write(company_branches)
st.write("- ### Carbon Offsets")
st.write(carbon_offsets)

st.write("## Total Information of the Branch")
st.write(f"Branch Name: {sel_branch_name}")
st.write(f"Branch ID: {sel_branch_id}")


# c_id = st.text_input('Company ID', '1')
# if st.button("Company"):
#     data = requests.get(f"http://service:80/companies/{c_id}").json()
#     st.write(pd.DataFrame([data]))
    
# c_id2 = st.text_input('Company ID ', '1')
# if st.button("branches"):
#     data = requests.get(f"http://service:80/branches/{c_id2}").json()
#     st.write(pd.DataFrame(data))