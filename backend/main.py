from fastapi import FastAPI

from .candidates import router as candidate_router


app = FastAPI(
    title="Intern Status Tracker",
    description="API for tracking intern candidates and their daily work status.",
    version="1.0.0"
)


app.include_router(candidate_router)


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