from typing import Optional
from sqlmodel import SQLModel, Field

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str
    skills: str = ""
    experience: str = ""
    education: str = ""
    