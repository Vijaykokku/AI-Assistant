import msal
import requests
import streamlit as st
import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")


AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Mail.Read"]


# ✅ Keep MSAL app alive across Streamlit reruns
@st.cache_resource
def get_msal_app():
    return msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY
    )


def get_access_token():

    app = get_msal_app()

    accounts = app.get_accounts()

    # ✅ Try silent login first
    if accounts:
        result = app.acquire_token_silent(
            SCOPES,
            account=accounts[0]
        )

        if result and "access_token" in result:
            return result["access_token"]

    # 🔐 Only happens first time
    result = app.acquire_token_interactive(
        scopes=SCOPES
    )

    return result["access_token"]


def get_unread_outlook_emails():

    try:
        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        url = (
            "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages"
            "?$filter=isRead eq false&$top=5"
        )

        response = requests.get(url, headers=headers)
        data = response.json()

        emails = []

        for mail in data.get("value", []):
            emails.append({
                "subject": mail["subject"],
                "sender": mail["from"]["emailAddress"]["address"],
                "snippet": mail["bodyPreview"]
            })

        return emails

    except Exception as e:
        st.error(e)
        return []