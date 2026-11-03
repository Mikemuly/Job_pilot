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