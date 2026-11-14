![Tests](https://github.com/Mikemuly/Job_pilot/actions/workflows/test.yml/badge.svg)
# Job_pilot
AI assistant that raeds your CV, builds your profile and (soon) matches you to jobs and drafts tailored applications. You approve everything before its sent

## Features

-  [x]  Upload a CV (PDF) and extract a structured profile with an LLM
-  [X]  Edit and save your profile in a web form
-  [x]  Fetch real jobs from a public job API (Remotive)
-  [x]  Rank jobs against your skills
-  [x]  AI explanation of why a job fits and whats's missing
-  [x]  AI drafted cover letters editable before use
-  [x]  Approval step before anything is saved as an application
-  [x]  Application tracker with statuses
-  [x]  Automated tests and CI on every push
-  [ ]  Smarter matching with embeddings
-  [ ]  Live demo


## Design decisions
- **Human in the loop.** The app drafts, you approve. Nothing is saved as an application until you click Approve, and the cover letter is editable first. This avoids low-quality mass applications and respects job board terms of service.
- **Prompt guardrails.** The cover letter prompt tells the model to use only facts from the profile, because invented experience in an application can hurt the candidate.
- **Simple matching first.** Matching starts as keyword overlap so it is fast, free and easy to test, and gives a baseline to improve with embeddings.
- **Partial updates.** Profile edits use PATCH so changing one field never wipes the others.
- **Duplicate protection.** Jobs amd applications are de-duplicated so repeated fetches or clicks don't create copies.
- **Tests that never call the AI.** The test suite uses an in-memory database amd avoids LLM calls, so CI is fast, free and needs no real API key.


## Limitations
- Matching is keyword-based, so related skills (for example "JS" vs "JavaScript") are not recognised yet.
- Jobs come from one source as of now (Remotive), which mostly lists remote roles. (Adding searching from the web soon)
- Applications are tracked, not aut-submitted.


## Tech Stack

- Python, FastAPI
- SQLite with SQLModel
- Streamlit (frontend)
- Groq API (LLM)
- pytest and Github Actions


## Setup

### Prerequisites

- Python 3.12 or newer
- Git
- A free Groq API key from https://console.groq.com/keys

### 1. Clone the repo

```bash
git clone https://github.com/Mikemuly/Job_pilot.git
cd Job_pilot```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.venv\Scripts\activate.ps1
```

Mac/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key

Copy the example file and edit it:

``bash
# Windows
copy .env.example .env
# Mac/Linux
cp .env.example .env
```

Open `.env` and set:

```
GROQ_API_KEY=your-secret-key
```

### 5. Start the app

You need two terminals, both in the project folder with '(.venv)` active.

Terminal 1, The API:

```bash
uvicorn main:app --reload
```

Terminal 2, the web interface:

```bash
streamlit run frontend.py
```
The app opens on https://localhost:8501

The database file `jobpilot.db` is created automatically on the first run.

## How to use it

1. **Get jobs:** enter a serach term (for example `python`) and click Fetch jobs.
2. **Upload your CV** as a PDF and click Extract profile.
3. **Check and edit** the extracted details, the save changes.
4. Click **Find matches** to see jobs ranked against your skills.
5. Click **Explain** to see why job fits and what is missing.
6. Click **Write cover letter**, edit it, then **Approve and save**
7. Track progress under **My applications**

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Powershell blocks the activate script | Run `Set-ExecutionPolicy -scope CurrentUser RemoteSigned`, then activate again |
| `ModuleNotFoundError` | The virtual environment is not active, or run `pip install -r requirements.txt` again |
| `429` or "no credits" from the AI | You hit the free tier limit. Wait a minuteand retry |
| `no such column` after pulling a new code | Stop the app, delete `job_pilot.db`, and start again (this clears saved data) |
| Streamlit says it cannot connect | Make sure uvicorn is running in the other terminal |