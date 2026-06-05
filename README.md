# 🤖 AI-Assisted Job Search Agent

An agentic job search tool that matches your resume against real job postings using LLMs and semantic search — exposed as a production REST API.

---

## 💡 Why I built this

Job searching is broken. You spend hours manually searching LinkedIn, Indeed, and Glassdoor — scrolling through hundreds of irrelevant postings that do not match your skills or experience level.

I built this to solve that problem for myself. Instead of manually filtering jobs, this agent reads your resume, understands your skills and experience level, searches real job postings via API, and automatically scores each posting against your profile — telling you exactly what you match and what you are missing.

The result: instead of 2 hours of manual job searching, you get ranked, matched job postings in under 60 seconds.

Built as a production REST API — not a toy demo — because real job search tools need to be reliable, fast, and integratable with other systems.

**Note on retrieval limit:**
The default is set to k=3 results intentionally — this project is built alongside active learning, so API calls are kept minimal to manage costs and rate limits during development. The JSearch API free tier allows up to 200 requests per month. If your only goal is maximum job retrieval, you can increase k to 50 or 100 per call — the architecture supports it with no code changes needed, just update the k parameter in your API call.

---

## 🎯 What it does

1. Upload your resume (PDF) via API
2. Enter your target role and location
3. Agent parses your resume and extracts your profile
4. Searches real job postings via JSearch API
5. Matches each job against your resume using GPT-4o-mini
6. Returns ranked results in 3 tiers:
   - Strong match (60%+)
   - Partial match (30-59%)
   - Fallback (role + location match only)

---

## 🔌 API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Check if API is running |
| POST | /search | Upload resume + get matched jobs |
| POST | /profile | Extract profile from resume only |
| GET | /jobs | Search jobs without resume |

---

## 🛠️ Tech stack

| Tool | Purpose |
|---|---|
| FastAPI | REST API framework |
| LangChain | LLM orchestration |
| LangSmith | LLM tracing and observability |
| ChromaDB | Vector storage for resume |
| JSearch API | Real job postings |
| GPT-4o-mini | Resume to job matching |
| HuggingFace | Sentence embeddings |
| Python | Core language |

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/ChandraShekar0209/AI-assisted-Job-Search.git
cd AI-assisted-Job-Search
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API keys

```bash
cp .env.example .env
```

Edit .env and add your keys:

```
OPENAI_API_KEY=your_openai_key_here
RAPIDAPI_KEY=your_rapidapi_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key_here
LANGCHAIN_PROJECT=job-search-agent
```

### 5. Run the API

```bash
uvicorn main:app --reload
```

Open interactive API docs at http://localhost:8000/docs

---

## 🧪 Example API call

```bash
curl -X POST "http://localhost:8000/search" \
  -F "role=AI Engineer" \
  -F "location=United States" \
  -F "k=3" \
  -F "resume=@myresume.pdf"
```

---

## 🔑 API keys needed

| Key | Where to get it |
|---|---|
| OpenAI API key | platform.openai.com |
| RapidAPI key | rapidapi.com — subscribe to JSearch free tier |
| LangSmith key | smith.langchain.com — free account |

---

## 📁 Project structure

```
AI-assisted-Job-Search/
├── src/
│   ├── __init__.py
│   ├── resume_parser.py    — PDF resume parser with ChromaDB
│   ├── job_search.py       — JSearch API integration
│   ├── job_matcher.py      — LLM resume to job matching
│   └── agent.py            — orchestrates everything + LangSmith tracing
├── main.py                 — FastAPI REST API
├── requirements.txt        — all dependencies
├── .env.example            — API key template
├── .gitignore
└── README.md
```

---

## 🧠 How the matching works

```
Resume PDF (uploaded via API)
    │
    ▼
PyPDF loader → ChromaDB → extract profile
    │
    ▼
JSearch API → fetch real job postings
    │
    ▼
GPT-4o-mini → score each job against profile
    │
    ▼
3-tier ranking:
Strong match (60%+)    → apply today
Partial match (30-59%) → apply and learn missing skills
Fallback (0-29%)       → apply based on role and location
    │
    ▼
LangSmith → traces every LLM call automatically
```

---

## 👤 Built by

Chandrashekar Garigapati
MS Data Science — SUNY Albany
BS Computer Science — SRM University

GitHub: https://github.com/ChandraShekar0209
