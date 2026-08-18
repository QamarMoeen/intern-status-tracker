from pydantic import BaseModel, EmailStr, Field
from datetime import date


class CandidateCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    training_track: str = Field(min_length=1, max_length=100)
    is_active: bool = True


class CandidateUpdate(BaseModel):
    full_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    training_track: str = Field(min_length=1, max_length=100)
    is_active: bool


class CandidateResponse(BaseModel):
    id: int
    full_name: str
    email: str
    training_track: str
    is_active: bool
    created_at: date