from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr]
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: Optional[str]
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = ""

class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    pinned: Optional[bool]
    archived: Optional[bool]

class NoteOut(BaseModel):
    id: str = Field(..., alias="_id")
    owner_id: str
    collaborators: List[str] = []
    title: str
    content: str
    pinned: bool
    archived: bool
    created_at: datetime
    updated_at: datetime
