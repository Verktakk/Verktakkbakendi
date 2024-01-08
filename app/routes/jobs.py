from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.database import SessionLocal
from app.db import schemas
from app.db import crud

router = APIRouter(
    prefix='/job',
    tags=['job']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

# Get all jobs
@router.get("/", response_model=schemas.JobListing)
async def read_jobs(db: db_dependency):
    db_jobs = await crud.get_joblistings(db)
    if db_jobs is None:
        raise HTTPException(status_code=404, detail="Jobs not found")
    return db_jobs

# Get a single job
@router.get("/{joblisting_id}", response_model=schemas.JobListing)
async def read_job(joblisting_id: int, db: db_dependency):
    db_job = await crud.get_joblisting(db, joblisting_id=joblisting_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job