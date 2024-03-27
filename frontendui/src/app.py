import streamlit as st
import requests


def main():

    st.title("Carbon Emissions Analytics Platform")
    message = st.text_input('Sample text input')

    if st.button('Sample API Call'):
        payload = {
            "text": message
        }
        res = requests.get(f"http://service:80/")
        with st.spinner('Getting result, please wait....'):
            st.write(res.json())


if __name__ == '__main__':
    main()
    
    