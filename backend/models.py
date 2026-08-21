from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.orm import relationship

from database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    training_track = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    statuses = relationship("DailyStatus", back_populates="candidate")

class DailyStatus(Base):
    __tablename__ = "daily_statuses"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column( Integer, ForeignKey("candidates.id"), nullable=False, index=True)
    status_date = Column(Date, nullable=False, index=True)
    work_completed = Column(Text,nullable=False)
    topics_learned = Column(Text,nullable=False)
    blockers = Column(Text,nullable=True)
    next_day_plan = Column(Text,nullable=False)
    completion_percentage = Column(Integer,nullable=False)
    created_at = Column(DateTime,default=lambda: datetime.now(timezone.utc),nullable=False)
    updated_at = Column( DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    candidate = relationship("Candidate", back_populates="statuses")
    __table_args__ = (
        UniqueConstraint("candidate_id", "status_date", name="unique_candidate_status_date"),
        )