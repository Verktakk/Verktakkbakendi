from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated
from app.db import crud
from app.db import models
from app.db import schemas
from app.db.database import SessionLocal, engine
import app.routes.auth as auth
import app.routes.profile as profileRouter
from logs.logging_config import setup_logging

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(profileRouter.router)
app.include_router(auth.router)

@app.on_event("startup")
def startup_event():
    setup_logging()

origins = [
    "http://localhost",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# used to make sure user is authenticated when accessing routes
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

@app.get("/users/", response_model=list[schemas.User])
async def read_users(db: db_dependency, skip: int = 0, limit: int = 100):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: db_dependency):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/joblistings/{joblisting_id}", response_model=schemas.JobListing)
async def read_joblisting(joblisting_id: int, db: db_dependency):
    db_joblisting = crud.get_joblisting(db, joblisting_id=joblisting_id)
    if db_joblisting is None:
        raise HTTPException(status_code=404, detail="JobListing not found")
    return db_joblisting

@app.get("/sellers/{seller_id}", response_model=schemas.Seller)
async def read_seller(seller_id: int, db: db_dependency):
    db_seller = crud.get_seller(db, seller_id=seller_id)
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return db_seller

@app.get("/reviews/{review_id}", response_model=schemas.Review)
async def read_review(review_id: int, db: db_dependency):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@app.get("/tags/{tag_id}", response_model=schemas.Tag)
async def read_tag(tag_id: int, db: db_dependency):
    db_tag = crud.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag



#@app.post("/users/{user_id}/items/", response_model=schemas.Item)
#def create_item_for_user(
#    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
#):
#    return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
#@app.get("/items/", response_model=list[schemas.Item])
#def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    items = crud.get_items(db, skip=skip, limit=limit)
#    return items