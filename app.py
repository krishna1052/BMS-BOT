import streamlit as st
from components.chat import display_chat, welcome_sidebar
from components.authentication import sign_in_with_google, handle_oauth_callback

def main(user):
    # st.set_page_config(page_title="CarsNodi.ai", page_icon="🚗", layout="wide")
    welcome_sidebar()
    display_chat(user)
    

if __name__ == "__main__":
    st.set_page_config(page_title="Hello", page_icon="👋")
    user = handle_oauth_callback()
    if user:
        st.query_params.clear()
        main(user)
    else:
        sign_in_with_google()
        st.cache_data.clear()
