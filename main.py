from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import create_db, get_session
from models import Profile

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



@app.get("/health")
def health():
    return {"status": "ok"}


