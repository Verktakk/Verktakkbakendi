from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db import schemas
from app.db import models
from app.db import crud
from constants import AppConfig

router = APIRouter(
    prefix='/profile',
    tags=['profile']
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/{profile_id}", response_model=schemas.Profile)
async def read_profile(profile_id: int, db: db_dependency):
    db_profile = crud.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@router.patch("/{profile_id}", response_model=schemas.Profile)
async def update_profile(profile_id: int, profile_data: schemas.ProfileUpdate, db: db_dependency):
    updated_profile = await crud.update_profile(db, profile_data, profile_id)
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated_profile