from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .candidates import router as candidate_router
from .statuses import router as status_router
from .dashboard import router as dashboard_router
from .database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Intern Status Tracker",
    description="API for tracking intern candidates and their daily work status.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidate_router)
app.include_router(status_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "message": "Intern Status Tracker API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }