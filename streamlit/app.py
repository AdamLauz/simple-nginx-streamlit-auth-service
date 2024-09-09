import requests
import streamlit as st
from urllib.parse import urlencode

AUTH_SERVICE_URL = "http://auth-service:3000"  # URL to the auth-service within Docker Compose network
MY_APP_URL = "http://localhost:8000"  # The URL where the user will return


def get_authentication_code():
    """Call auth-service to exchange code for token."""
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}/authentication", allow_redirects=True)

        if response.status_code == 200:
            pass
        else:
            st.error(f"Failed to get code: {response.status_code}")
    except Exception as e:
        st.error(f"Error connecting to auth-service: {e}")


def get_authentication_token(code):
    """Call auth-service to exchange code for token, following the redirect."""
    try:
        # Make a request to the auth-service with the code and allow redirects
        response = requests.get(f"{AUTH_SERVICE_URL}/authentication/login?code={code}", allow_redirects=True)

        if response.status_code == 200:
            # The service will redirect with a new URL that contains the token in the query string
            final_url = response.url

            # Extract the token from the final redirected URL
            parsed_url = requests.utils.urlparse(final_url)
            query_params = requests.utils.parse_qs(parsed_url.query)

            # Extract the token from the query parameters
            token = query_params.get('token', [None])[0]
            if token:
                return token
            else:
                st.error("No token found in the redirected URL")
                return None
        else:
            st.error(f"Failed to get token: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error connecting to auth-service/login: {e}")
        return None


# Check if the user has returned with a code from the external service

code = st.session_state.get("code", st.experimental_get_query_params().get('code'))

st.write(code)


if code:
    token = st.session_state.get("token", get_authentication_token(code))
    if token:
        st.session_state.token = token
        st.success(f"Login successful! Token: {token}")
    else:
        st.session_state.code = code
        # The user has returned from the external service with a code, exchange it for a token
        st.write(f"Authentication successful! Received code: {code}")
        # You can now send this code to the auth-service to exchange it for a token.

else:
    # No code present, so start the authentication process
    get_authentication_code()





