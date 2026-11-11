from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from database import create_db, get_session
from models import Profile, ProfileUpdate
from pypdf import PdfReader
from ai import extract_profile, explain_match, write_cover_letter
from models import Profile, ProfileUpdate, Job
from jobs import fetch_jobs
from matching import score_job


app = FastAPI(title="JobPilot")

@app.on_event("startup")
def on_startup():
    create_db()

@app.post("/profiles")
def create_profile(profile: Profile, session: Session = Depends(get_session)):
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile

@app.get("/profiles")
def list_profiles(session: Session = Depends(get_session)):
    return session.exec(select(Profile)).all()

@app.get("/profiles/{profile_id}")
def get_profile(profile_id: int, session: Session = Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404,detail="Profile not found")
    return profile

@app.post("/upload_cv")
async def upload_cv(
    file :UploadFile = File(...),
    session: Session = Depends(get_session),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    reader = PdfReader(file.file)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    data = extract_profile(text)
    profile = Profile(
        full_name= str(data.get("full_name", "")),
        email= str(data.get("email", "")),
        skills= str(data.get("skills", "")),
        experience= str(data.get("experience", "")),
        education= str(data.get("education", "")),
    
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile

@app.patch("/profiles/{profile_id}")
def update_profile(
    profile_id: int,
    updates: ProfileUpdate,
    session: Session= Depends(get_session),

):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)


    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile

@app.post("/jobs/fetch")
def fetch_and_save_jobs(search: str, session: Session= Depends(get_session)):
    saved = 0
    for j in fetch_jobs(search, 20):
        source_id = str (j["id"])
        exists = session.exec (select(Job).where(Job.source_id == source_id)).first()
        if exists:
            continue
        session.add(
            Job(
                source_id = source_id,
                title = j["title"],
                company = j["company_name"],
                location = j.get("candidate_require_location", ""),
                url = j["url"],
                description = j.get("description", ""),
            )
        )
        saved += 1
    session.commit()
    return {"saved": saved}

@app.get("/jobs")
def list_jobs(session: Session = Depends(get_session)):
    return session.exec(select(Job)).all()          


@app.get("/profile/{profile_id}/matches")
def get_matches(profile_id: int, session: Session = Depends(get_session)):
    profile= session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code =404, detail="Profile not found")

    results = []
    for job in session.exec(select(Job)).all():
        result = score_job(profile.skills, f"{job.title} {job.description}")
        results.append(
            {
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "url": job.url,
                "score": result["score"],
                "matched": result["matched"],
            }
        )
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:10]

@app.get("/profiles/{profile_id}/explain/{job_id}")
def explain(
    profile_id: int,
    job_id: int,
    session: Session = Depends(get_session),
):
    profile = session.get(Profile, profile_id)
    job = session.get(Job, job_id)
    if not profile or not job:
        raise HTTPException(status_code=404, detail="Profile or job not found")

    text = explain_match(
        profile.skills, profile.experience, job.title, job.description
    )
    return {"explanation": text}

@app.post("/profile/{profile_id}/cover-letter/{job_id}")
def cover_letter(
    profile_id: int,
    job_id: int,
    session: Session = Depends(get_session),
):
    profile = session.get(Profile, profile_id)
    job = session.get(Job, job_id)
    if not profile or not job:
        raise HTTPException(status_code=404, detail="Profile or job not found")

    letter = write_cover_letter(
        profile.full_name,
        profile.skills,
        profile.experience,
        profile.education,
        job.title,
        job.company,
        job.description,
    )
    return {"cover_letter": letter}


@app.get("/health")
def health():
    return {"status": "ok"}


