import requests
import streamlit as st
from urllib.parse import urlencode

AUTH_SERVICE_URL = "http://auth-service:3000"  # URL to the auth-service within Docker Compose network
MY_APP_URL = "http://nginx:8000"  # The URL where the user will return


def get_authentication_code():
    """Call auth-service to exchange code for token."""
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}/authentication")

        if response.status_code == 200:
            return response.json().get('token')
        else:
            st.error(f"Failed to get token: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error connecting to auth-service: {e}")
        return None


def get_authentication_token(code):
    """Call auth-service to exchange code for token."""
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}/authentication/login?code={code}", allow_redirects=True)

        if response.status_code == 200:
            return response.json().get('token')
        else:
            st.error(f"Failed to get token: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error connecting to auth-service: {e}")
        return None


def redirect_to_auth_service():
    """Redirect the user to the external authentication service via auth-service."""
    try:
        # Call the auth-service to initiate the authentication flow
        # Pass the redirect URL (our app's URL) as a parameter
        params = {'redirect_to_url': MY_APP_URL}
        auth_url = f"{AUTH_SERVICE_URL}/authentication?{urlencode(params)}"

        # Redirect the user to the external authentication URL
        st.markdown(f"<meta http-equiv='refresh' content='0; url={auth_url}' />", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error initiating authentication: {e}")


def main():
    # Check if the user has returned with a code from the external service
    code = st.experimental_get_query_params().get('code')

    if code:
        # The user has returned from the external service with a code, exchange it for a token
        st.write(f"Authentication successful! Received code: {code}")
        # You can now send this code to the auth-service to exchange it for a token.

        token = get_authentication_token(code)
        if token:
            st.success(f"Login successful! Token: {token}")
    else:
        # No code present, so start the authentication process
        redirect_to_auth_service()
