from datetime import date

from fastapi import APIRouter, HTTPException

from .schemas import CandidateCreate, CandidateUpdate, CandidateResponse


router = APIRouter(
    prefix="/api/candidates",
    tags=["Candidates"]
)


candidates = []
next_candidate_id = 1


@router.post("/", response_model=CandidateResponse, status_code=201)
def create_candidate(candidate: CandidateCreate):
    global next_candidate_id

    new_candidate = {
        "id": next_candidate_id,
        "full_name": candidate.full_name,
        "email": candidate.email,
        "training_track": candidate.training_track,
        "is_active": candidate.is_active,
        "created_at": date.today()
    }

    candidates.append(new_candidate)
    next_candidate_id += 1

    return new_candidate


@router.get("/", response_model=list[CandidateResponse])
def get_candidates():
    return candidates


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int):
    for candidate in candidates:
        if candidate["id"] == candidate_id:
            return candidate

    raise HTTPException(
        status_code=404,
        detail="Candidate not found"
    )


@router.put("/{candidate_id}", response_model=CandidateResponse)
def update_candidate(
    candidate_id: int,
    candidate_data: CandidateUpdate
):
    for candidate in candidates:
        if candidate["id"] == candidate_id:
            candidate["full_name"] = candidate_data.full_name
            candidate["email"] = candidate_data.email
            candidate["training_track"] = candidate_data.training_track
            candidate["is_active"] = candidate_data.is_active

            return candidate

    raise HTTPException(
        status_code=404,
        detail="Candidate not found"
    )


@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int):
    for index, candidate in enumerate(candidates):
        if candidate["id"] == candidate_id:
            candidates.pop(index)

            return {
                "message": "Candidate deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Candidate not found"
    )