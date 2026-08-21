from fastapi import APIRouter, HTTPException

from .database import db_dependency
from .models import Candidate
from .schemas import CandidateCreate, CandidateUpdate, CandidateResponse


router = APIRouter(
    prefix="/api/candidates",
    tags=["Candidates"]
)


@router.post("/", response_model=CandidateResponse, status_code=201)
def create_candidate(candidate_data: CandidateCreate, db: db_dependency):
    new_candidate = Candidate(
        full_name=candidate_data.full_name,
        email=candidate_data.email,
        training_track=candidate_data.training_track,
        is_active=candidate_data.is_active
    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return new_candidate


@router.get("/", response_model=list[CandidateResponse])
def get_candidates(db: db_dependency):
    return db.query(Candidate).all()


@router.get("/{candidate_id}", response_model=CandidateResponse
)
def get_candidate(candidate_id: int, db: db_dependency):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return candidate


@router.put("/{candidate_id}", response_model=CandidateResponse)
def update_candidate(
    candidate_id: int,
    candidate_data: CandidateUpdate,
    db: db_dependency
):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    candidate.full_name = candidate_data.full_name
    candidate.email = candidate_data.email
    candidate.training_track = candidate_data.training_track
    candidate.is_active = candidate_data.is_active

    db.commit()
    db.refresh(candidate)

    return candidate

@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: db_dependency):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    db.delete(candidate)
    db.commit()

    return {
        "message": "Candidate deleted successfully"
    }