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
    ["companies", "branches", "carbon_offsets", "carbon_emissions_sources", "carbon_regulations", "carbon_sequestration", "footsprints"])

st.markdown('____')
if sel_table == 'companies':
    st.subheader('Company')       
    company = requests.get("http://service:80/companies/").json()
    if len(company) == 0:
        st.write(f"No companies found")
        st.stop()
    company = pd.DataFrame(company)
    company.sort_values(by=['id'], inplace=True, ignore_index=True)
    
    company_col = ['id'] + [col for col in company.columns.values if col != 'id']
    company = company[company_col]    

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
    
    branches_col = ['id'] + [col for col in branches.columns.values if col != 'id']
    branches = branches[branches_col] 

    
    branches_ed = st.experimental_data_editor(branches, hide_index=True, num_rows="dynamic", disabled=["id"], key="edit_branches")
    
    edit_branches_data = st.session_state["edit_branches"]
    
    if st.button('Update Branch Data'):
        for row_idx in edit_branches_data['deleted_rows']:
            b_id = branches.loc[row_idx,['id']].values[0]
            req = requests.delete(f'http://service:80/branch/{b_id}', headers={'accept': 'application/json'})
            if req.status_code == 200:
                st.write(f"Deleted branch with id: {b_id}, branch_name: {branches.loc[row_idx,['branch_name']].values[0]}")
            else:
                st.write(f"Failed to delete branch with id: {b_id}")
    
    
        headers = {'accept': 'application/json','Content-Type': 'application/json'}
        for added_row in edit_branches_data['added_rows']:
            req = requests.post(f'http://service:80/branches', headers=headers, json=added_row)
            if req.status_code == 200:
                st.write(f"Added branch with branch_name: {added_row['branch_name']}")
            else:
                st.write(f"Failed to add branch with branch_name: {added_row['branch_name']}")
                
        for row_idx in edit_branches_data['edited_rows']:
            b_id = branches.loc[row_idx,['id']].values[0]
            updated_row = edit_branches_data['edited_rows'][row_idx]
            req = requests.put(f'http://service:80/branch/{b_id}', headers=headers, json=updated_row)
            if req.status_code == 200:
                st.write(f"Updated branch with id: {b_id}, branch_name: {updated_row['branch_name']}")     
            else:
                st.write(f"Failed to update branch with id: {b_id}")

        
        st.session_state.pop('edit_branches', None)
        

if sel_table == 'carbon_offsets':
    st.subheader('Carbon Offset')  
    
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
    


    carbon_offset = requests.get(f"http://service:80/companies/{sel_comp_id}/carbon_offsets").json()
    if len(carbon_offset) == 0:
        st.write(f"No carbon offsets found for company: {sel_comp_name}")
        st.stop()
    carbon_offset = pd.DataFrame(carbon_offset)
    carbon_offset.sort_values(by=['id'], inplace=True, ignore_index=True)
    carbon_offset_col = ['id'] + [col for col in carbon_offset.columns.values if col != 'id']
    carbon_offset = carbon_offset[carbon_offset_col]
    offset_type_options = ['renewable_energy_projects', 'reforestation']
    carbon_offset["offset_type"] = carbon_offset["offset_type"].map({str(i+1):op for i,op in enumerate(offset_type_options) })
    
    carbon_offset_ed = st.experimental_data_editor(carbon_offset, hide_index=True, num_rows="dynamic", disabled=["id"], key="edit_carbon_offset")
    
    edit_carbon_offset_data = st.session_state["edit_carbon_offset"]
    
    if st.button('Update Carbon Offset Data'):

        headers = {'accept': 'application/json','Content-Type': 'application/json'}
        for added_row in edit_carbon_offset_data['added_rows']:
            if added_row['offset_type'] in ['renewable_energy_projects', 'reforestation']:
                req = requests.post(f'http://service:80/carbon_offset', headers=headers, json=added_row)
                if req.status_code == 200:
                    st.write(f"Added branch with branch_name: {added_row['offset_type']}")
            else:
                st.write(f"Invalid offset type: {added_row['offset_type']}")
            


        for row_idx in edit_carbon_offset_data['edited_rows']:
            # b_id = carbon_offset.loc[row_idx,['id']].values[0]
            updated_row = edit_carbon_offset_data['edited_rows'][row_idx]
            res = carbon_offset.loc[row_idx,:].to_dict()
            res[str(list(updated_row.keys())[0])] = list(updated_row.values())[0]
            co_id = int(res['id'])
            req = requests.put(f'http://service:80/carbon_offset/{co_id}', headers=headers, json=res)
            if req.status_code == 200:
                st.write(f"Updated carbon offset with id: {co_id}, offset_type: {res['offset_type']}")
            else:
                st.write(f"Failed to update carbon offset with id: {co_id}, offset_type: {res['offset_type']}")
                
                
        for row_idx in edit_carbon_offset_data['deleted_rows']:
            co_id = carbon_offset.loc[row_idx,['id']].values[0]
            req = requests.delete(f'http://service:80/carbon_offset/{co_id}', headers={'accept': 'application/json'})
            if req.status_code == 200:
                st.write(f"Deleted carbon offset with id: {co_id}")
            else:
                st.write(f"Failed to delete carbon offset with id: {co_id}")
                

        st.session_state.pop('edit_branches', None)
        
# if sel_table == 'carbon_emissions_sources':
    # st.subheader('Carbon Emissions Sources') 
    
    # col1, col2 = st.columns(2)
    
    # with col1:
    #     company = requests.get("http://service:80/companies/").json()
    #     if len(company) == 0:
    #         st.write(f"No companies found")
    #         st.stop()
    #     company = pd.DataFrame(company)
    #     company_name = sorted(company["c_name"].tolist())

    #     sel_comp_name = st.selectbox(
    #         'Select a Company:',
    #         company_name)
    #     sel_comp_id = company[company["c_name"] == sel_comp_name]["id"].values[0]
    
    # with col2:
    #     branches = requests.get(f"http://service:80/companies/{sel_comp_id}/branches").json()
    #     if len(branches) == 0:
    #         st.write(f"No branches found for company: {sel_comp_name}")
    #         st.stop()
    #     branches = pd.DataFrame(branches)
    #     branches.sort_values(by=['id'], inplace=True, ignore_index=True)
    #     branches_col = ['id'] + [col for col in branches.columns.values if col != 'id']
    #     branches = branches[branches_col] 
    #     branch_name = sorted(branches["branch_name"].tolist())

    #     sel_branch_name = st.selectbox(
    #         'Select a Branch:',
    #         branch_name)
    #     sel_branch_id = branches[branches["branch_name"] == sel_branch_name]["id"].values[0]
        
    # st.write(f"Selected Company: {sel_comp_name}, Selected Branch: {sel_branch_name}")
        
        
def post_carbon_regulations(added_rows):
    headers = {'accept': 'application/json','Content-Type': 'application/json'}
    for added_row in added_rows:
            req = requests.post(f'http://service:80/regulations', headers=headers, json=added_row)
            if req.status_code == 200:
                st.write(f"Added regulation with regulation_name: {added_row['regulation_name']}")
            else:
                st.write(f"Failed to add regulation with regulation_name: {added_row['regulation_name']}")
                

if sel_table == 'carbon_regulations':
    st.subheader("Carbon Regulations")
    carbon_regulations = requests.get("http://service:80/regulations/").json()
    if len(carbon_regulations) == 0:
        st.write(f"No carbon regulations found")
        # st.stop()
        carbon_regulations = [{"regulation_name": "None","description": "None", "id": 1}]
        
    carbon_regulations = pd.DataFrame(carbon_regulations)
    carbon_regulations.sort_values(by=['id'], inplace=True, ignore_index=True)
    
    carbon_regulations_col = ['id'] + [col for col in carbon_regulations.columns.values if col != 'id']
    carbon_regulations = carbon_regulations[carbon_regulations_col]    

    carbon_regulations_col_ed = st.experimental_data_editor(carbon_regulations, hide_index=True, num_rows="dynamic", disabled=["id"], key="edit_carbon_regulations")
    
    edit_carbon_regulations = st.session_state["edit_carbon_regulations"]
    # st.write(st.session_state["edit_company"]) # 👈 Show the value in Session State

        
    if st.button('Update Company Data'):
        if len(edit_carbon_regulations['added_rows']) > 0:
            post_carbon_regulations(edit_carbon_regulations['added_rows'])
        
    
    
#     curl -X 'GET' \
#   'http://localhost:8001/regulations/?skip=0&limit=100' \
#   -H 'accept: application/json'
    
    
#     curl -X 'POST' \
#   'http://localhost:8001/regulations/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "regulation_name": "test",
#   "description": "test"
# }'