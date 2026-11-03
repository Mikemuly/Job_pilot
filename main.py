from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from database import create_db, get_session
from models import Profile
from pypdf import PdfReader
from ai import extract_profile

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
async def upload_cv(file :UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    reader = PdfReader(file.file)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    return extract_profile(text)


          



@app.get("/health")
def health():
    return {"status": "ok"}


