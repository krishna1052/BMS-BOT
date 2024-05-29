
import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Define your Google OAuth credentials from .env
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_CALLBACK_URI = os.getenv("GOOGLE_CALLBACK_URI")


def sign_in_with_google():
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        "scope=email%20profile&"
        f"response_type=code&"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_CALLBACK_URI}"
    )
    col1a, col1b, col2, col3a, col3b = st.columns([2,2,2,2,2])
    
    gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, red, orange);
    background: linear-gradient(to right, red, orange);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 3em;
}
</style>
<div class="gradient-text">BMS-BOT</div>
"""

    
    
    chatbot_title = st.empty()
    
    st.markdown(gradient_text_html, unsafe_allow_html=True)
    st.write("Welcome to BMS-BOT, an application that is here to help you with your queries. Please feel free to ask any questions and I will try to help you as best as I can.")   
    with col2:
        
        # col2a, col2b, col2c = st.columns([2,1,2])
        # chatbot_title.write("Welcome to BMS-BOT", )
        st.image("assets/logo.jpg", use_column_width="always",)
    with col3b:
        google_link = st.empty()
        google_link.link_button("Sign In", auth_url, type="primary", use_container_width=True)

@st.cache_data
def handle_oauth_callback():
    if st.query_params.get_all("code"):
        code = st.query_params["code"]
        st.query_params.clear()
        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_CALLBACK_URI,
            "grant_type": "authorization_code",
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}  # Add the header
        response = requests.post(token_url, data=payload, headers=headers)
        data = response.json()


        if response.ok:
            return get_user_details(data["access_token"])
        else:
            st.error(f"Token exchange failed: {data}")
            st.link_button("Home", "/", type="primary")
            return None
    else:
        return None

def get_user_details(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    profile_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    response = requests.get(profile_url, headers=headers)
    user = response.json()
    if response.ok:
        return user
    else:
        st.error(f"Failed to fetch user details: {user}")
        st.link_button("Home", "/", type="primary")
        return None
