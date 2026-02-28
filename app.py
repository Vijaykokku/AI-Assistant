import streamlit as st
from outlook_service import get_unread_outlook_emails
from ai_processor import analyze_email, generate_reply, generate_daily_focus, analyze_jira
from jira_service import get_my_jira_issues
from auth import login
from ai_processor import pick_next_best_task
from datetime import datetime, date

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(layout="wide")
st.title("🤖 AI Work Assistant")

# ---------------- LOGIN ---------------- #

user, access_token = login()
if not user:
    st.stop()

email = user.get("mail") or user.get("userPrincipalName")
st.success(f"Welcome {email} 👋")
st.caption("🔐 Signed in with Microsoft Entra ID")

# ---------------- SIDEBAR ---------------- #

st.sidebar.image("logo.png", use_container_width=True)
page = st.sidebar.radio("Navigation", ["📧 Emails", "🎫 Jira", "📊 Today"])

metrics_container = st.container()

# ---------------- SESSION STATE ---------------- #

defaults = {
    "email_analyzed": False,
    "jira_analyzed": False,
    "jira_ai_output": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- CACHED AI ---------------- #

@st.cache_data
def cached_analyze_email(text):
    return analyze_email(text)

@st.cache_data
def cached_generate_focus(email_summaries, jira_summaries):
    return generate_daily_focus(email_summaries, jira_summaries)

@st.cache_data
def cached_analyze_jira(text):
    return analyze_jira(text)

@st.cache_data
def cached_pick_task(jira_text):
    return pick_next_best_task(jira_text)

# ---------------- FETCH DATA ---------------- #

emails = get_unread_outlook_emails()
issues = get_my_jira_issues()

# ---------------- JIRA GLOBAL COUNTS ---------------- #

jira_todo = 0
jira_in_progress = 0
jira_high = 0
jira_medium = 0
jira_overdue = 0
jira_summaries = []

today = date.today()

for issue in issues:

    status = issue["status"].lower()
    priority = issue["priority"].lower()
    due_date_raw = issue.get("due_date")

    jira_summaries.append(
        f"{issue['key']} {issue['summary']} {issue['status']} {issue['priority']}"
    )

    # ---------- STATUS ----------
    if status in ["to do", "todo", "backlog", "open", "selected for development"]:
        jira_todo += 1

    elif status in ["in progress", "in review", "code review", "development"]:
        jira_in_progress += 1

    # ---------- PRIORITY ----------
    if priority in ["high", "highest"]:
        jira_high += 1
    elif priority == "medium":
        jira_medium += 1

    # ---------- OVERDUE ----------
    if due_date_raw:
        due_date_obj = datetime.strptime(due_date_raw, "%Y-%m-%d").date()
        if due_date_obj < today:
            jira_overdue += 1

# ---------------- EMAIL ANALYSIS GLOBAL ---------------- #

email_summaries = []
needs_reply_emails = []
reply_count = high_count = medium_count = 0

def get_urgency(result_text):
    for line in result_text.split("\n"):
        if "urgency" in line.lower():
            if "high" in line.lower():
                return "high"
            elif "medium" in line.lower():
                return "medium"
    return "low"

if st.session_state.email_analyzed and emails:

    for email_item in emails:

        result = cached_analyze_email(
            email_item["subject"] + " " + email_item["snippet"]
        )

        email_summaries.append(result)

        if "reply needed: yes" in result.lower():
            reply_count += 1
            needs_reply_emails.append((email_item, result))

        urgency = get_urgency(result)

        if urgency == "high":
            high_count += 1
        elif urgency == "medium":
            medium_count += 1

# ---------------- TOP METRICS ---------------- #

with metrics_container:

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col4.metric("🎫 In Progress", jira_in_progress)
    col5.metric("📌 To Do", jira_todo)
    col6.metric("⏰ Overdue", jira_overdue)

    if st.session_state.email_analyzed:
        col1.metric("🔴 Needs Reply", reply_count)
        col2.metric("🟠 Medium", medium_count)
        col3.metric("🚨 High", high_count)
    else:
        col1.metric("🔴 Needs Reply", "-")
        col2.metric("🟠 Medium", "-")
        col3.metric("🚨 High", "-")

# ===================== EMAIL PAGE ===================== #

if page == "📧 Emails":

    st.header("📧 Work Emails")

    if st.button("🧠 Analyze Emails"):
        st.session_state.email_analyzed = True
        st.rerun()

    if not emails:
        st.info("No unread emails 🎉")

    for email_item in emails:

        st.subheader(email_item["subject"])
        st.write(f"From: {email_item['sender']}")
        st.write(email_item["snippet"])

        if st.session_state.email_analyzed:

            result = cached_analyze_email(
                email_item["subject"] + " " + email_item["snippet"]
            )

            urgency = get_urgency(result)

            if urgency == "high":
                st.error(result)
            elif urgency == "medium":
                st.warning(result)
            else:
                st.success(result)

            if "reply needed: yes" in result.lower():
                if st.button(f"✍️ Generate Reply for {email_item['subject']}"):
                    reply = generate_reply(
                        email_item["subject"] + " " + email_item["snippet"]
                    )
                    st.text_area("Draft Reply", reply, height=200)

        else:
            st.info("Click 'Analyze Emails' to run AI.")

        st.divider()

# ===================== JIRA PAGE ===================== #

if page == "🎫 Jira":

    st.header("🎫 My Jira Tickets")

    if st.button("🧠 Analyze Jira"):

        jira_text = "\n".join(jira_summaries)

        with st.spinner("Analyzing your sprint workload..."):
            st.session_state.jira_ai_output = cached_analyze_jira(jira_text)

        st.session_state.jira_analyzed = True
        st.rerun()

    if st.session_state.jira_ai_output:
        st.success(st.session_state.jira_ai_output)

    if st.session_state.jira_analyzed:

        st.subheader("📊 Jira Insights")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📌 To Do", jira_todo)
        c2.metric("🚧 In Progress", jira_in_progress)
        c3.metric("🔥 High", jira_high)
        c4.metric("🟠 Medium", jira_medium)

    else:
        st.info("Click 'Analyze Jira' to generate sprint insights.")

    for issue in issues:

        st.subheader(f"{issue['key']} — {issue['summary']}")

        # ---------- PRIORITY COLOR ----------
        priority = issue["priority"].lower()

        if priority in ["high", "highest"]:
            priority_view = f"🔴 {issue['priority']}"
        elif priority == "medium":
            priority_view = f"🟠 {issue['priority']}"
        elif priority in ["low", "lowest"]:
            priority_view = f"🟢 {issue['priority']}"
        else:
            priority_view = f"⚪ {issue['priority']}"

        # ---------- DUE DATE LOGIC ----------
        due_date_raw = issue.get("due_date")

        if due_date_raw:
            due_date_obj = datetime.strptime(due_date_raw, "%Y-%m-%d").date()

            if due_date_obj < today:
                due_view = f"🔴 Overdue — {due_date_raw}"

            elif due_date_obj == today:
                due_view = f"🟠 Due Today — {due_date_raw}"

            else:
                days_left = (due_date_obj - today).days
                due_view = f"🟢 Due in {days_left} days — {due_date_raw}"

        else:
            due_view = "⚪ No due date"

        # ---------- CARD LAYOUT ----------
        col1, col2, col3 = st.columns(3)

        col1.write(f"📌 Status: {issue['status']}")
        col2.write(f"🔥 Priority: {priority_view}")
        col3.write(f"📅 {due_view}")

        st.divider()

# ===================== TODAY PAGE ===================== #

if page == "📊 Today":

    st.header("🧠 My Focus Today")

    # ---------------- GUARD RAIL ---------------- #

    if not st.session_state.email_analyzed and not st.session_state.jira_analyzed:
        st.warning("Run Email or Jira analysis to generate your daily plan.")
        st.stop()

    # ---------------- SESSION STATE ---------------- #

    if "daily_focus_output" not in st.session_state:
        st.session_state.daily_focus_output = None

    if "next_task_output" not in st.session_state:
        st.session_state.next_task_output = None

    # ---------------- GENERATE DAILY FOCUS ---------------- #

    if st.button("📌 Generate my daily focus"):

        focus_input = f"""
        EMAIL PRIORITY
        Needs reply: {reply_count}
        High urgency: {high_count}
        Medium urgency: {medium_count}

        JIRA WORKLOAD
        In Progress: {jira_in_progress}
        To Do: {jira_todo}

        Jira Details:
        {jira_summaries}
        """

        with st.spinner("Thinking about your day..."):
            st.session_state.daily_focus_output = cached_generate_focus(
                focus_input, ""
            )

        st.rerun()

    # ---------------- SHOW DAILY FOCUS ---------------- #

    import re

    if st.session_state.daily_focus_output:

        st.subheader("📅 Your execution plan")

        raw_lines = st.session_state.daily_focus_output.split("\n")

        sections = []
        current_section = []

        # ---------- GROUP LINES INTO SECTIONS ----------
        for line in raw_lines:
            clean = line.strip()

            if not clean:
                continue

            if any(keyword in clean.lower() for keyword in
                    ["immediate attention", "plan next", "main focus today"]):

                if current_section:
                    sections.append(current_section)

                current_section = [clean]

            else:
                current_section.append(clean)

        if current_section:
            sections.append(current_section)

        # ---------- RENDER IN COLORED BLOCKS ----------
        for section in sections:

            title = re.sub(r'^[^\w]+', '', section[0])
            content = " ".join(section[1:])

            block_text = f"**{title}**  \n{content}"

            lower = title.lower()

            if "immediate attention" in lower:
                st.error(f"🔥 {block_text}")

            elif "plan next" in lower:
                st.warning(f"📌 {block_text}")

            elif "main focus today" in lower:
                st.success(f"🎯 {block_text}")

            else:
                st.info(block_text)

    st.divider()

    # ---------------- NEXT BEST TASK ---------------- #

    st.subheader("🚀 What should I start next?")

    if st.button("Suggest my next task"):

        jira_text = "\n".join(jira_summaries)

        with st.spinner("Choosing the best task for you..."):
            st.session_state.next_task_output = cached_pick_task(jira_text)

        st.rerun()

    if st.session_state.next_task_output:

        st.subheader("✅ Recommended for you")

        st.info(st.session_state.next_task_output)