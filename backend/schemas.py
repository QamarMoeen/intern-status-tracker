from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date


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
    created_at: datetime

    class Config:
        from_attributes = True  


class DailyStatusCreate(BaseModel):
    candidate_id: int
    status_date: date
    work_completed: str = Field(min_length=1)
    topics_learned: str = Field(min_length=1)
    blockers: str | None = None
    next_day_plan: str = Field(min_length=1)
    completion_percentage: int = Field(
        ge=0,
        le=100
    )


class DailyStatusUpdate(BaseModel):
    candidate_id: int
    status_date: date
    work_completed: str = Field(min_length=1)
    topics_learned: str = Field(min_length=1)
    blockers: str | None = None
    next_day_plan: str = Field(min_length=1)
    completion_percentage: int = Field(
        ge=0,
        le=100
    )


class DailyStatusResponse(BaseModel):
    id: int
    candidate_id: int
    candidate_name : str
    status_date: date
    work_completed: str
    topics_learned: str
    blockers: str | None
    next_day_plan: str
    completion_percentage: int

    class Config:
            from_attributes = True 