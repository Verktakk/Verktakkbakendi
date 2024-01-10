from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db import schemas
from app.db import models
from app.db import crud
from constants import AppConfig

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Búa til user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_test_user(db: db_dependency, create_user_request: schemas.UserCreate):
        print(create_user_request.profile)
        user = models.User(
            email=create_user_request.email,
            phone_number=create_user_request.phone_number,
            profile = models.Profile(**create_user_request.profile.model_dump()),
    )
        db.add(user)
        db.commit()

# Get a single user
@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: db_dependency):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user