from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from .database import get_db
from .models import Candidate, DailyStatus


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def get_dashboard_summary(
    date: date = Query(...),
    db: Session = Depends(get_db)
):
    # ---------------------------------
    # 1. Get all active candidates
    # ---------------------------------

    active_candidates = (
        db.query(Candidate)
        .filter(Candidate.is_active == True)
        .all()
    )

    # ---------------------------------
    # 2. Get statuses for selected date
    # ---------------------------------

    selected_statuses = (
        db.query(DailyStatus)
        .filter(DailyStatus.status_date == date)
        .all()
    )

    # Candidate IDs who submitted on selected date
    submitted_candidate_ids = {
        status.candidate_id
        for status in selected_statuses
    }

    # ---------------------------------
    # 3. Submitted candidates
    # ---------------------------------

    submitted_candidates = []

    for status in selected_statuses:

        candidate = next(
            (
                candidate
                for candidate in active_candidates
                if candidate.id == status.candidate_id
            ),
            None
        )

        if candidate:
            submitted_candidates.append({
                "candidate_id": candidate.id,
                "candidate_name": candidate.full_name,
                "completion_percentage":
                    status.completion_percentage,
                "status_date": status.status_date
            })

    # Sort highest completion first
    submitted_candidates.sort(
        key=lambda candidate:
            candidate["completion_percentage"],
        reverse=True
    )

    # ---------------------------------
    # 4. Missing candidates
    # ---------------------------------

    missing_candidates = []

    for candidate in active_candidates:

        if candidate.id not in submitted_candidate_ids:

            missing_candidates.append({
                "candidate_id": candidate.id,
                "candidate_name": candidate.full_name,
                "email": candidate.email
            })

    # ---------------------------------
    # 5. Average completion
    # ---------------------------------

    average_completion = (
        db.query(
            func.avg(
                DailyStatus.completion_percentage
            )
        )
        .filter(
            DailyStatus.status_date == date
        )
        .scalar()
    )

    if average_completion is None:
        average_completion = 0
    else:
        average_completion = round(
            float(average_completion),
            2
        )

    # ---------------------------------
    # 6. Latest status from every
    #    candidate who has a status
    # ---------------------------------

    all_candidates = (
        db.query(Candidate)
        .filter(Candidate.is_active == True)
        .all()
    )

    latest_statuses = []

    for candidate in all_candidates:

        latest_status = (
            db.query(DailyStatus)
            .filter(
                DailyStatus.candidate_id == candidate.id
            )
            .order_by(
                DailyStatus.status_date.desc()
            )
            .first()
        )

        # Only include candidates
        # who actually have a status
        if latest_status:

            latest_statuses.append({
                "candidate_id": candidate.id,
                "candidate_name": candidate.full_name,
                "status_date": latest_status.status_date,
                "completion_percentage":
                    latest_status.completion_percentage
            })

    # Sort by completion percentage
    latest_statuses.sort(
        key=lambda candidate:
            candidate["completion_percentage"],
        reverse=True
    )

    # ---------------------------------
    # 7. Return dashboard
    # ---------------------------------

    return {
        "date": date,

        "total_active_candidates":
            len(active_candidates),

        "submitted_count":
            len(submitted_candidates),

        "missing_count":
            len(missing_candidates),

        "average_completion_percentage":
            average_completion,

        "submitted_candidates":
            submitted_candidates,

        "missing_candidates":
            missing_candidates,

        "latest_statuses":
            latest_statuses
    }