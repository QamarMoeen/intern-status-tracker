from datetime import date

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from database import db_dependency
from models import Candidate, DailyStatus
from schemas import (
    DailyStatusCreate,
    DailyStatusResponse,
    DailyStatusUpdate
)


router = APIRouter(
    prefix="/api/statuses",
    tags=["Daily Statuses"]
)

def status_response(status: DailyStatus):
    return {
        "id": status.id,
        "candidate_id": status.candidate_id,
        "candidate_name": status.candidate.full_name,
        "status_date": status.status_date,
        "work_completed": status.work_completed,
        "topics_learned": status.topics_learned,
        "blockers": status.blockers,
        "next_day_plan": status.next_day_plan,
        "completion_percentage": status.completion_percentage,
        "created_at": status.created_at,
        "updated_at": status.updated_at
    }

@router.get("/", response_model=list[DailyStatusResponse])
def get_statuses(
    db: db_dependency,
    candidate_id: int | None = None,
    status_date: date | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
):
    query = db.query(DailyStatus)

    if candidate_id is not None:
        query = query.filter(DailyStatus.candidate_id == candidate_id)

    if status_date is not None:
        query = query.filter(DailyStatus.status_date == status_date)

    if date_from is not None:
        query = query.filter(DailyStatus.status_date >= date_from)

    if date_to is not None:
        query = query.filter(DailyStatus.status_date <= date_to)

    statuses = query.order_by(DailyStatus.status_date.desc()).all()

    for status in statuses:
        status.candidate_name = status.candidate.full_name

    return statuses



@router.get("/{status_id}", response_model=DailyStatusResponse
)
def get_status(status_id: int, db: db_dependency):

    status = db.query(DailyStatus).filter(DailyStatus.id == status_id).first()

    if status is None:
        raise HTTPException(
            status_code=404,
            detail="Status not found"
        )
    status.candidate_name = status.candidate.full_name
    return status_response(status)


@router.post("/",response_model=DailyStatusResponse, status_code=201)
def create_status(status_data: DailyStatusCreate, db: db_dependency):

    candidate = db.query(Candidate).filter(Candidate.id == status_data.candidate_id).first()

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    if status_data.status_date > date.today():
        raise HTTPException(
            status_code=400,
            detail="Status date cannot be in the future"
        )

    new_status = DailyStatus(**status_data.model_dump())

    db.add(new_status)

    try:
        db.commit()
        db.refresh(new_status)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Candidate already has a status for this date"
        )
    new_status.candidate_name = new_status.candidate.full_name
    return new_status

@router.put("/{status_id}", response_model=DailyStatusResponse)
def update_status(
    status_id: int,
    status_data: DailyStatusUpdate,
    db: db_dependency
):
    status = db.query(DailyStatus).filter(DailyStatus.id == status_id).first()

    if status is None:
        raise HTTPException(
            status_code=404,
            detail="Status not found"
        )

    candidate = db.query(Candidate).filter(Candidate.id == status_data.candidate_id).first()

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    if status_data.status_date > date.today():
        raise HTTPException(
            status_code=400,
            detail="Status date cannot be in the future"
        )    

    status.candidate_id = status_data.candidate_id
    status.status_date = status_data.status_date
    status.work_completed = status_data.work_completed
    status.topics_learned = status_data.topics_learned
    status.blockers = status_data.blockers
    status.next_day_plan = status_data.next_day_plan
    status.completion_percentage = status_data.completion_percentage

    try:
        db.commit()
        db.refresh(status)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Candidate already has a status for this date"
        )
    status.candidate_name = status.candidate.full_name
    return status


@router.delete("/{status_id}")
def delete_status(status_id: int, db: db_dependency):

    status = db.query(DailyStatus).filter(DailyStatus.id == status_id).first()

    if status is None:
        raise HTTPException(
            status_code=404,
            detail="Status not found"
        )

    db.delete(status)
    db.commit()

    return {
        "message": "Status deleted successfully"
    }