import os
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")


def get_my_jira_issues():

    url = f"{JIRA_BASE_URL}/rest/api/3/search/jql"

    jql = """
    (
        assignee = currentUser()
        OR reporter = currentUser()
    )
    AND statusCategory != Done
    ORDER BY priority DESC, updated DESC
    """

    payload = {
        "jql": jql,
        "maxResults": 20,
        "fields": ["summary", "status", "priority", "duedate"]
    }

    try:
        response = requests.post(
            url,
            json=payload,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        if response.status_code != 200:
            st.error(f"Jira API Error: {response.status_code}")
            st.json(response.json())
            return []

        data = response.json()

        issues = []

        for issue in data.get("issues", []):

            fields = issue["fields"]

            issues.append({
                "key": issue["key"],
                "summary": fields.get("summary", "No summary"),
                "status": fields.get("status", {}).get("name", "Unknown"),
                "priority": fields.get("priority", {}).get("name", "None"),
                "due_date": issue["fields"].get("duedate", "No due date")
            })

        return issues

    except Exception as e:
        st.error(f"Jira connection failed: {e}")
        return []