import logging
from sqlalchemy.orm import Session
from . import models
from . import schemas

# User CRUD
async def get_user(db: Session, user_id: int):
    return await db.query(models.User).filter(models.User.id == user_id).first()

async def get_user_by_email(db: Session, email: str):
    return await db.query(models.User).filter(models.User.email == email).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return await db.query(models.User).offset(skip).limit(limit).all()

# Profile CRUD
async def get_profile(db: Session, profile_id: int):
    return await db.query(models.Profile).filter(models.Profile.id == profile_id).first()

async def update_profile(db: Session, profile_data: schemas.ProfileUpdate, profile_id: int):
    profile = await db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if profile is None:
        return False
    for key, value in profile_data.model_dump(exclude_unset=True):
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

async def create_user_profile(db: Session, profile: schemas.ProfileCreate, user_id: int):
    db_profile = models.Profile(**profile.dict(), owner_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# Seller CRUD
async def get_seller(db: Session, skip: int = 0, limit: int = 100):
    return await db.query(models.Seller).offset(skip).limit(limit).all()

async def create_seller(db: Session, seller: schemas.SellerCreate, profile_id: int):
    db_seller = models.Seller(**seller.dict(), profile_id=profile_id)
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

# Review CRUD
async def get_review(db: Session, skip: int = 0, limit: int = 100):
    return await db.query(models.Review).offset(skip).limit(limit).all()

async def create_review(db: Session, review: schemas.ReviewCreate, profile_id: int):
    db_review = models.Review(**review.dict(), profile_id=profile_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# Tag CRUD
async def get_tag(db: Session, skip: int = 0, limit: int = 100):
    return await db.query(models.Tag).offset(skip).limit(limit).all()

async def create_tag(db: Session, tag: schemas.TagCreate, joblisting_id: int):
    db_tag = models.Tag(**tag.dict(), joblisting_id=joblisting_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

# JobListing CRUD
async def get_joblistings(db: Session, skip: int = 0, limit: int = 100):
    return await db.query(models.JobListing).offset(skip).limit(limit).all()

async def get_joblisting(db: Session, joblisting_id: int):
    return await db.query(models.JobListing).filter(models.JobListing.id == joblisting_id).first()

async def create_joblisting(db: Session, joblisting: schemas.JobListingCreate, seller_id: int):
    db_joblisting = models.JobListing(**joblisting.dict(), seller_id=seller_id)
    db.add(db_joblisting)
    db.commit()
    db.refresh(db_joblisting)
    return db_joblisting

# JobListingTagAssociation CRUD - SPA I SEINNA
# def get_joblistingtagassociation(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.JobListingTagAssociation).offset(skip).limit(limit).all()

# def associate_tag_with_joblisting(db: Session, joblistingtagassociation: schemas.JobListingTagAssociationCreate, joblisting_id: int, tag_id: int):
#     db_joblistingtagassociation = models.JobListingTagAssociation(**joblistingtagassociation.dict(), joblisting_id=joblisting_id, tag_id=tag_id)
#     db.add(db_joblistingtagassociation)
#     db.commit()
#     db.refresh(db_joblistingtagassociation)
#     return db_joblistingtagassociation