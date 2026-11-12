from typing import Optional
from sqlmodel import SQLModel, Field

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str
    skills: str = ""
    experience: str = ""
    education: str = ""


class ProfileUpdate(SQLModel):
    full_name: Optional [str] = None
    email: Optional [str] = None
    skills: Optional [str] = None
    experience: Optional [str] = None
    education: Optional [str] = None


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key = True)
    source_id: str =Field(index=True, unique=True)
    title:str
    company:str
    location:str = ""
    url:str
    description:str = ""

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id")
    job_id: int = Field(foreign_key="job.id")
    status: str = "saved"
    cover_letter: str = ""
    
