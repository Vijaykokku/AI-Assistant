import ollama

MODEL = "llama3.2"


# ================= EMAIL ANALYSIS ================= #

def analyze_email(text):

    prompt = f"""
You are an AI work assistant.

Analyze the email and return STRICTLY in this format:

Summary: <one line>
Urgency: High / Medium / Low
Reply Needed: Yes / No

Email:
{text}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


# ================= EMAIL REPLY ================= #

def generate_reply(text):

    prompt = f"""
Write a professional, concise reply.

Keep a polite corporate tone.

Email:
{text}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


# ================= DAILY FOCUS ================= #

def generate_daily_focus(email_summary_text, jira_summary_text):

    prompt = f"""
You are an AI productivity assistant.

WORK CONTEXT

EMAILS:
{email_summary_text}

JIRA:
{jira_summary_text}

Give output in this format:

🔥 Immediate Attention:
📌 Plan Next:
🎯 Main Focus Today:

Keep it short, practical, and executive-level.
"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


# ================= JIRA ANALYSIS ================= #

def analyze_jira(jira_text):

    prompt = f"""
You are an AI Agile delivery assistant.

Analyze this Jira workload.

Return in this format:

Sprint Health: Light / Balanced / Overloaded

Key Risks:
- ...

Recommended Focus Today:
- ...

Quick Wins:
- ...

Jira Data:
{jira_text}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

# ================= BEST TASK PICKER ================= #

def pick_next_best_task(jira_summaries):

    prompt = f"""
You are an AI engineering manager.

From the Jira list below, choose the SINGLE best task to start now.

Rules:
- Prefer In Progress tasks
- Otherwise pick highest priority
- Otherwise pick something small & actionable

Return in this format:

Next Task:
Why:
Expected Outcome:

Jira:
{jira_summaries}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]