# app/main.py
import streamlit as st
from utils.config import Config
from ui.home import render_home_page
from ui.summary import main as render_summary_page
from ui.help_resources import main as render_help_page
from ui.prompts import main as render_prompts_page
from ui.user_settings import display_settings as render_user_settings_page
from utils.helpers import setup_logging
import logging

# Set page config early
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.FAVICON_URL,
    layout="wide"
)

# Initialize logging
setup_logging()

def main():
    try:
        # Add a selectbox for navigation
        page = st.sidebar.selectbox(
            "Select Page",
            ["Home", "Summary", "Help", "Prompts", "User Settings"]
        )

        # Render the selected page
        if page == "Home":
            render_home_page()
        elif page == "Summary":
            render_summary_page()
        elif page == "Help":
            render_help_page()
        elif page == "Prompts":
            render_prompts_page()
        elif page == "User Settings":
            render_user_settings_page()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error in main: {e}")

if __name__ == "__main__":
    main()





# auth/api.py: Handle all API interactions with Authentik and Shlink.
# auth/encryption.py: Manage encryption and decryption functionalities.
# ui/forms.py: Render and handle user input forms.
# ui/home.py: Manage the main UI components and layout.
# utils/config.py: Centralize configuration management.
# messages.py: Handle user-facing messages and notifications.
