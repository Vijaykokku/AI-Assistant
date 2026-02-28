# 🤖 AI Work Assistant – Personal Execution Copilot

An AI-powered productivity assistant that connects your **Outlook emails** and **Jira sprint workload**, analyzes them using a **local LLM**, and generates a **daily execution plan with the next best task to work on**.

---

## 🚀 Problem Statement

Modern professionals lose significant time every day:

- Reading and prioritizing emails
- Switching between inbox and Jira
- Deciding what to work on next

This leads to:

❌ Context switching  
❌ Missed priorities  
❌ Reactive work instead of focused execution  
❌ Cognitive overload  

There is no intelligent system that understands both **communication and delivery workload together**.

---

## 💡 Solution

AI Work Assistant acts as your **personal execution copilot**.

It:

- Reads unread Outlook emails
- Fetches your assigned Jira tickets
- Uses AI to:
  - Detect urgency
  - Detect reply requirement
  - Generate summaries
- Produces:
  - 📊 Smart workload insights
  - 📅 Daily execution plan
  - 🚀 Next best task recommendation

---

## 🧠 Key Features

### 📧 Email Intelligence
- Urgency detection (High / Medium / Low)
- Reply-needed detection
- AI-generated reply drafts
- Clean priority visualization

### 🎫 Jira Intelligence
- Sprint workload analysis
- Status-based metrics
- Priority-based metrics
- ⏰ Overdue detection
- 📅 Due-date awareness

### 📊 Unified Dashboard
Single interface for:
- Communication
- Delivery
- Daily execution

### 🧭 Daily Focus Generator
AI converts raw data → **actionable execution plan**

### 🚀 Next Best Task Engine
AI tells you:
> “Start with this task now.”

---

## 🏗️ Architecture Overview

### Components

- Streamlit UI
- Microsoft Entra ID Authentication (MSAL)
- Outlook Service (Microsoft Graph API)
- Jira Service (Jira REST API)
- AI Processor (Ollama – local LLM)
- Session State Manager

### Flow

User Login → Fetch Emails & Jira → AI Analysis → Metrics → Execution Plan

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI Engine
- Ollama (Llama 3.2 – runs locally)

### Authentication
- Microsoft Entra ID (MSAL)

### APIs
- Microsoft Graph API
- Jira REST API

### Environment Management
- python-dotenv

---

## 🔐 Security

- Microsoft secure OAuth login
- Access tokens cached locally
- Secrets stored in `.env`
- No hardcoded credentials

---

## 📂 Project Structure


ai-work-assistant/
│
├── app.py
├── auth.py
├── outlook_service.py
├── jira_service.py
├── ai_processor.py
├── logo.png
├── requirements.txt
├── .env.example
└── README.md


---

## ⚙️ Setup Instructions

1) Clone the repository
```bash
git clone https://github.com/your-repo/ai-work-assistant.git
cd ai-work-assistant

---

2️) Create virtual environment
python -m venv venv
venv\Scripts\activate

---

3️)Install dependencies
pip install -r requirements.txt

---

4️)Configure environment variables

Create a .env file:

CLIENT_ID=
TENANT_ID=

JIRA_BASE_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=

---

5️) Run Ollama
ollama run llama3.2

6️)Start the app
streamlit run app.py

---

🖥️ Demo Flow

Login using Microsoft work account
Analyze Emails → view urgency + AI replies
Analyze Jira → view sprint insights + overdue tasks
Generate Daily Focus → AI execution plan
Suggest Next Task → AI recommends what to do now

---

📊 Sample Insights
Top Metrics
🔴 Emails needing reply
🚨 High urgency emails
🎫 Jira in progress
⏰ Overdue tasks

AI Execution Plan
🔥 Immediate Attention
📌 Plan Next
🎯 Main Focus Today

---

⚔️ Challenges & Solutions
Challenge	Solution
Repeated login	MSAL token caching
Slow AI response	On-demand analysis
Jira workflow variety	Flexible status mapping
Output formatting	Structured AI parsing

---

🌟 Impact

⏱ Saves 30–60 minutes per day
🧠 Reduces cognitive load
📈 Improves execution speed
🎯 Data-driven prioritization

---

🔮 Future Enhancements
Calendar integration
Team workload dashboard
Auto-refresh AI insights
SaaS deployment
RAG over company knowledge base