# app/utils/config.py
import os
from dotenv import load_dotenv
import logging
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine the absolute path to the root directory
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# Path to the .env file
env_path = os.path.join(ROOT_DIR, '.env')

# Load environment variables from the .env file
load_dotenv(dotenv_path=env_path)

class Config:
    AUTHENTIK_API_TOKEN = os.getenv("AUTHENTIK_API_TOKEN")
    MAIN_GROUP_ID = os.getenv("MAIN_GROUP_ID")
    BASE_DOMAIN = os.getenv("BASE_DOMAIN")
    FLOW_ID = os.getenv("FLOW_ID")
    LOCAL_DB = os.getenv("LOCAL_DB", "users.csv")
    SHLINK_API_TOKEN = os.getenv("SHLINK_API_TOKEN")
    SHLINK_URL = os.getenv("SHLINK_URL")
    AUTHENTIK_API_URL = os.getenv("AUTHENTIK_API_URL")
    PAGE_TITLE = os.getenv("PAGE_TITLE", "Authentik Streamlit App")
    FAVICON_URL = os.getenv("FAVICON_URL", "default_favicon.ico")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
    WEBHOOK_ENABLED = os.getenv("WEBHOOK_ENABLED", "true").lower() == "true"
    INDIVIDUAL_WEBHOOKS = {
        "user_created": os.getenv("WEBHOOK_USER_CREATED", "true").lower() == "true",
        "password_reset": os.getenv("WEBHOOK_PASSWORD_RESET", "true").lower() == "true",
        # Add more webhook types as needed
    }
    # # Log loaded environment variables (mask sensitive data)
    # logger.info("Loaded Environment Variables:")
    # logger.info(f"AUTHENTIK_API_TOKEN: {'****' if AUTHENTIK_API_TOKEN else None}")
    # logger.info(f"MAIN_GROUP_ID: {MAIN_GROUP_ID}")
    # logger.info(f"BASE_DOMAIN: {BASE_DOMAIN}")
    # logger.info(f"FLOW_ID: {FLOW_ID}")
    # # logger.info(f"ENCRYPTION_KEY: {'****' if ENCRYPTION_KEY else None}")  # Commented out
    # logger.info(f"SHLINK_API_TOKEN: {'****' if SHLINK_API_TOKEN else None}")
    # logger.info(f"SHLINK_URL: {SHLINK_URL}")
    # logger.info(f"AUTHENTIK_API_URL: {AUTHENTIK_API_URL}")
    # logger.info(f"PAGE_TITLE: {PAGE_TITLE}")
    # logger.info(f"FAVICON_URL: {FAVICON_URL}")
    # logger.info(f"WEBHOOK_URL: {WEBHOOK_URL}")
    # logger.info(f"WEBHOOK_SECRET: {WEBHOOK_SECRET}")

    # Validate critical configurations
    required_vars = {
        "AUTHENTIK_API_TOKEN": AUTHENTIK_API_TOKEN,
        "MAIN_GROUP_ID": MAIN_GROUP_ID,
        "BASE_DOMAIN": BASE_DOMAIN,
        "FLOW_ID": FLOW_ID,
        "LOCAL_DB": LOCAL_DB,
        "SHLINK_API_TOKEN": SHLINK_API_TOKEN,
        "SHLINK_URL": SHLINK_URL,
        "AUTHENTIK_API_URL": AUTHENTIK_API_URL,
        "WEBHOOK_URL": WEBHOOK_URL,
        "WEBHOOK_SECRET": WEBHOOK_SECRET
    }
    
    missing_vars = [var_name for var_name, var in required_vars.items() if var is None]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Initialize Fernet outside the Config class
# Completely remove or comment out the following lines
# try:
#     fernet = Fernet(Config.ENCRYPTION_KEY)
# except Exception as e:
#     raise ValueError(f"Invalid ENCRYPTION_KEY: {e}")

def save_settings(
    webhook_enabled, user_created_webhook, password_reset_webhook, selected_theme, shlink_url,
    auth0_domain, auth0_callback_url, auth0_authorize_url, auth0_token_url, authentik_api_url,
    webhook_url, authentik_api_token, shlink_api_token, main_group_id, flow_id, encryption_password, webhook_secret
):
    # Implement the logic to save the settings
    Config.WEBHOOK_ENABLED = webhook_enabled
    Config.INDIVIDUAL_WEBHOOKS["user_created"] = user_created_webhook
    Config.INDIVIDUAL_WEBHOOKS["password_reset"] = password_reset_webhook
    Config.SHLINK_URL = shlink_url
    os.environ["AUTH0_DOMAIN"] = auth0_domain
    os.environ["AUTH0_CALLBACK_URL"] = auth0_callback_url
    os.environ["AUTH0_AUTHORIZE_URL"] = auth0_authorize_url
    os.environ["AUTH0_TOKEN_URL"] = auth0_token_url
    Config.AUTHENTIK_API_URL = authentik_api_url
    Config.WEBHOOK_URL = webhook_url
    if authentik_api_token != "****":
        Config.AUTHENTIK_API_TOKEN = authentik_api_token
    if shlink_api_token != "****":
        Config.SHLINK_API_TOKEN = shlink_api_token
    Config.MAIN_GROUP_ID = main_group_id
    Config.FLOW_ID = flow_id
    if encryption_password != "****":
        os.environ["ENCRYPTION_PASSWORD"] = encryption_password
    if webhook_secret != "****":
        Config.WEBHOOK_SECRET = webhook_secret
    os.environ["STREAMLIT_THEME"] = selected_theme
    # Add any additional logic needed to persist these changes

def display_settings():
    st.title("Automation Settings")

    # Group settings into expandable sections
    with st.expander("Webhook Settings"):
        # Toggle for enabling/disabling all webhooks
        webhook_enabled = st.checkbox("Enable Webhooks", value=Config.WEBHOOK_ENABLED)
        
        # Toggles for individual webhooks
        st.subheader("Individual Webhook Settings")
        user_created_webhook = st.checkbox("User Created Webhook", value=Config.INDIVIDUAL_WEBHOOKS["user_created"])
        password_reset_webhook = st.checkbox("Password Reset Webhook", value=Config.INDIVIDUAL_WEBHOOKS["password_reset"])
        
        # Webhook URL and Secret
        webhook_url = st.text_input("Webhook URL", value=Config.WEBHOOK_URL or "")
        webhook_secret = st.text_input("Webhook Secret", value="****" if Config.WEBHOOK_SECRET else "", type="password")

    with st.expander("Environment Variables"):
        # General settings
        st.subheader("General Settings")
        theme_options = ["light", "dark", "auto"]
        current_theme = os.getenv("STREAMLIT_THEME", "auto")
        selected_theme = st.selectbox("Color Theme", options=theme_options, index=theme_options.index(current_theme))
        # Auth0 settings
        st.subheader("Auth0 Settings")
        auth0_domain = st.text_input("Auth0 Domain", value=os.getenv("AUTH0_DOMAIN", ""))
        auth0_callback_url = st.text_input("Auth0 Callback URL", value=os.getenv("AUTH0_CALLBACK_URL", ""))
        auth0_authorize_url = st.text_input("Auth0 Authorize URL", value=os.getenv("AUTH0_AUTHORIZE_URL", ""))
        auth0_token_url = st.text_input("Auth0 Token URL", value=os.getenv("AUTH0_TOKEN_URL", ""))

        # Authentik settings
        st.subheader("Authentik Settings")
        authentik_api_url = st.text_input("Authentik API URL", value=Config.AUTHENTIK_API_URL or "")
        authentik_api_token = st.text_input("Authentik API Token", value="****" if Config.AUTHENTIK_API_TOKEN else "", type="password")

        # Shlink settings
        st.subheader("Shlink Settings")
        shlink_url = st.text_input("Shlink URL", value=Config.SHLINK_URL or "")
        shlink_api_token = st.text_input("Shlink API Token", value="****" if Config.SHLINK_API_TOKEN else "", type="password")

        # Other settings
        st.subheader("Other Settings")
        main_group_id = st.text_input("Main Group ID", value=Config.MAIN_GROUP_ID or "")
        flow_id = st.text_input("Flow ID", value=Config.FLOW_ID or "")
        encryption_password = st.text_input("Encryption Password", value="****" if os.getenv("ENCRYPTION_PASSWORD") else "", type="password")

    # Save settings (this would typically involve updating environment variables or a config file)
    if st.button("Save Settings"):
        # Logic to save the settings
        save_settings(
            webhook_enabled, user_created_webhook, password_reset_webhook, selected_theme, shlink_url,
            auth0_domain, auth0_callback_url, auth0_authorize_url, auth0_token_url, authentik_api_url,
            webhook_url, authentik_api_token, shlink_api_token, main_group_id, flow_id, encryption_password, webhook_secret
        )
        st.success("Settings saved successfully!")
