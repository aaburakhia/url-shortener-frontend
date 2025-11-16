import streamlit as st
import requests
import json

API_ENDPOINT = "https://jgb8c6f5wi.execute-api.us-east-2.amazonaws.com/"

st.set_page_config(page_title="URL Shortener", layout="centered")

st.title("Serverless URL Shortener")
st.write("A simple frontend for my AWS serverless application.")

# --- Form for creating a new short URL ---
with st.form("shorten_form"):
    long_url_input = st.text_input("Long URL", placeholder="https://example.com/my-very-long-url")
    submitted = st.form_submit_button("Shorten!")

    if submitted:
        if not long_url_input:
            st.warning("Please enter a URL.")
        else:
            # This is where we call your AWS Backend
            payload = json.dumps({"longUrl": long_url_input})
            headers = {"Content-Type": "application/json"}
            
            try:
                response = requests.post(API_ENDPOINT, data=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    short_id = result.get('shortId')
                    short_url = f"{API_ENDPOINT}{short_id}"
                    
                    st.success("Success! Here is your short URL:")
                    st.code(short_url, language="text")
                else:
                    st.error(f"Error: Could not shorten URL. The API returned status code: {response.status_code}")
                    st.json(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while connecting to the API: {e}")
