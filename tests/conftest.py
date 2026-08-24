import pytest

from database import SessionLocal
from models import Candidate, DailyStatus


@pytest.fixture(autouse=True)
def clean_database():
    db = SessionLocal()

    try:
        db.query(DailyStatus).delete()
        db.query(Candidate).delete()
        db.commit()

        yield

    finally:
        db.close()