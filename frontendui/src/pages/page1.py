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

{cv.page1_description}
"""
)


col1, col2 = st.columns(2)

with col1:
    company = requests.get("http://service:80/companies/").json()
    company = pd.DataFrame(company)
    company_name = sorted(company["c_name"].tolist())

    sel_comp_name = st.selectbox(
        'Companies',
        company_name)
    sel_comp_id = company[company["c_name"] == sel_comp_name]["id"].values[0]

with col2:
    company_branches = requests.get(f"http://service:80/companies/{sel_comp_id}/branches").json() 
    company_branches = pd.DataFrame(company_branches)
    company_branches_name = sorted(company_branches["branch_name"].tolist())

    sel_branch_name = st.selectbox(
        'branches',
        company_branches_name)
    sel_branch_id = company_branches[company_branches["branch_name"] == sel_branch_name]["id"].values[0]


carbon_offsets = requests.get(f"http://service:80/companies/{sel_comp_id}/carbon_offsets/").json()
carbon_offsets = pd.DataFrame(carbon_offsets)

number_of_branches = len(company_branches)


company_summary = requests.get(f"http://service:80/company/{sel_comp_id}/summary/").json()

st.write("## Total Information of the Company")
st.markdown('____')
company_info = {"Company Name": sel_comp_name, 
                "Company ID": sel_comp_id, 
                "Total number of branches": number_of_branches,
                "Total Carbon Emissions": company_summary["total_emissions"],
                "Total Sequestrations": company_summary["total_sequestrations"],
                "Total Carbon Offsets": carbon_offsets["offset_amount"].sum(),
                }
company_info = pd.DataFrame([company_info])
st.write(f"- ### Company Info")
st.markdown(company_info.style.hide(axis="index").to_html(), unsafe_allow_html=True)
st.write("- ### Company Branches")
st.markdown(company_branches.style.hide(axis="index").to_html(), unsafe_allow_html=True)
# st.write(company_branches)
st.write("- ### Carbon Offsets")
# st.write(carbon_offsets)
st.markdown(carbon_offsets.style.hide(axis="index").to_html(), unsafe_allow_html=True)


st.write(" ")
st.write(" ")
st.write("## Total Information of the Branch")
st.markdown('____')


branch_summary = requests.get(f"http://service:80/baranch/{sel_branch_id}/summary/").json()


branch_info = {"Branch Name": sel_branch_name, 
                "Branch ID": sel_branch_id, 
                # "Total number of branches": number_of_branches,
                "Total Carbon Emissions": branch_summary["total_emissions"],
                "Total Sequestrations": branch_summary["total_sequestrations"],
                # "Total Carbon Offsets": carbon_offsets["offset_amount"].sum(),
                }
branch_info = pd.DataFrame([branch_info])

st.write(f"- ### Branch Info")
st.markdown(branch_info.style.hide(axis="index").to_html(), unsafe_allow_html=True)
st.write("- ### Emission Sources")

emissionssources = requests.get(f"http://service:80/branch/{sel_branch_id}/emissionssources/").json()
emissionssources = pd.DataFrame(emissionssources)
st.markdown(emissionssources.style.hide(axis="index").to_html(), unsafe_allow_html=True)



