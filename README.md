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
