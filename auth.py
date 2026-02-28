import streamlit as st
import msal
import os
import requests

CLIENT_ID = "4336ed17-0db1-4eba-8391-a44cc087e580"
TENANT_ID = "648ca8d9-38e9-44ca-bc27-20e5a79ee859"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read", "Mail.Read"]

CACHE_FILE = "token_cache.bin"


# ---------------- TOKEN CACHE ---------------- #

def load_cache():
    cache = msal.SerializableTokenCache()
    if os.path.exists(CACHE_FILE):
        cache.deserialize(open(CACHE_FILE, "r").read())
    return cache


def save_cache(cache):
    if cache.has_state_changed:
        open(CACHE_FILE, "w").write(cache.serialize())


# ---------------- MSAL APP ---------------- #

@st.cache_resource
def get_msal_app():
    cache = load_cache()

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache
    )

    return app, cache


# ---------------- GET USER PROFILE ---------------- #

def get_user_profile(access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers=headers
    )

    return response.json()


# ---------------- LOGIN FUNCTION ---------------- #

def login():

    app, cache = get_msal_app()

    # ---------- LOGIN SCREEN UI ---------- #

def login():

    # ✅ If already logged in this session → reuse
    if "user" in st.session_state and "access_token" in st.session_state:
        return st.session_state.user, st.session_state.access_token

    app, cache = get_msal_app()

    st.markdown("### 🔐 Secure Login")
    st.caption("Sign in with your work account to continue")

    if st.button("Sign in with Microsoft"):

        result = app.acquire_token_interactive(
            scopes=SCOPES,
            prompt="select_account"
        )

        if "access_token" in result:

            save_cache(cache)

            user_profile = get_user_profile(result["access_token"])

            # ✅ STORE IN SESSION
            st.session_state.user = user_profile
            st.session_state.access_token = result["access_token"]

            st.rerun()

    return None, None