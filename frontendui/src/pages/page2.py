from navigation import make_sidebar
import streamlit as st
import requests
from utils import const_variable as cv
import pandas as pd


st.header(cv.project_title, divider=cv.header_color)
make_sidebar()

st.write(
    f"""
# {cv.page2_title}

{cv.page2_description}
"""
)

st.write("## Select a Table to Edit")
sel_table = st.selectbox(
    'Tables:',
    ["companies", "branches", "carbon_offsets", "emission_sources", "regulations", "carbon_sequestration", "footsprints"])

st.markdown('____')
if sel_table == 'companies':
    st.subheader('Company')       
    company = requests.get("http://service:80/companies/").json()
    if len(company) == 0:
        st.write(f"No companies found")
        st.stop()
    company = pd.DataFrame(company)
    company.sort_values(by=['id'], inplace=True, ignore_index=True)
    
    company_ed = st.experimental_data_editor(company, hide_index=True, num_rows="dynamic", disabled=["id"], key="edit_company")
    
    edit_company_data = st.session_state["edit_company"]
    # st.write(st.session_state["edit_company"]) # 👈 Show the value in Session State

    
    if st.button('Update Company Data'):
        for row_idx in edit_company_data['deleted_rows']:
            c_id = company.loc[row_idx,['id']].values[0]
            req = requests.delete(f'http://service:80/company/{c_id}', headers={'accept': 'application/json'})
            if req.status_code == 200:
                st.write(f"Deleted company with id: {c_id}, c_name: {company.loc[row_idx,['c_name']].values[0]}")
            
        headers = {'accept': 'application/json','Content-Type': 'application/json'}
        for added_row in edit_company_data['added_rows']:
            req = requests.post(f'http://service:80/companies', headers=headers, json=added_row)
            if req.status_code == 200:
                st.write(f"Added company with c_name: {added_row['c_name']}")
     
        for row_idx in edit_company_data['edited_rows']:
            c_id = company.loc[row_idx,['id']].values[0]
            updated_row = edit_company_data['edited_rows'][row_idx]
            req = requests.put(f'http://service:80/company/{c_id}', headers=headers, json=updated_row)
            if req.status_code == 200:
                st.write(f"Updated company with id: {c_id}, c_name: {updated_row['c_name']}")
        
        st.session_state.pop('edit_company', None)
        

if sel_table == 'branches':
    st.subheader('Branch')       
    
    company = requests.get("http://service:80/companies/").json()
    if len(company) == 0:
        st.write(f"No companies found")
        st.stop()
    company = pd.DataFrame(company)
    company_name = sorted(company["c_name"].tolist())

    sel_comp_name = st.selectbox(
        'Select a Company:',
        company_name)
    sel_comp_id = company[company["c_name"] == sel_comp_name]["id"].values[0]
    
    
    branches = requests.get(f"http://service:80/companies/{sel_comp_id}/branches").json()
    if len(branches) == 0:
        st.write(f"No branches found for company: {sel_comp_name}")
        st.stop()
    branches = pd.DataFrame(branches)
    branches.sort_values(by=['id'], inplace=True, ignore_index=True)
    
    
    branches_ed = st.experimental_data_editor(branches, hide_index=True, num_rows="dynamic", disabled=["id"], key="edit_branches")
    
    edit_branches_data = st.session_state["edit_branches"]
    
    if st.button('Update Branch Data'):
        for row_idx in edit_branches_data['deleted_rows']:
            b_id = branches.loc[row_idx,['id']].values[0]
            req = requests.delete(f'http://service:80/branch/{b_id}', headers={'accept': 'application/json'})
            if req.status_code == 200:
                st.write(f"Deleted branch with id: {b_id}, branch_name: {branches.loc[row_idx,['branch_name']].values[0]}")
    
    
        headers = {'accept': 'application/json','Content-Type': 'application/json'}
        for added_row in edit_branches_data['added_rows']:
            req = requests.post(f'http://service:80/branches', headers=headers, json=added_row)
            if req.status_code == 200:
                st.write(f"Added branch with branch_name: {added_row['branch_name']}")
                
        for row_idx in edit_branches_data['edited_rows']:
            b_id = branches.loc[row_idx,['id']].values[0]
            updated_row = edit_branches_data['edited_rows'][row_idx]
            req = requests.put(f'http://service:80/branch/{b_id}', headers=headers, json=updated_row)
            if req.status_code == 200:
                st.write(f"Updated branch with id: {b_id}, branch_name: {updated_row['branch_name']}")     

        
        st.session_state.pop('edit_branches', None)
        

if sel_table == 'carbon_offsets':
    st.subheader('Carbon Offset')  
    
    
    
      'http://localhost:8001/companies/1/carbon_offsets/?skip=0&limit=100' \
#