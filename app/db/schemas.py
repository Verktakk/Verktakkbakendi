from pydantic import BaseModel
from typing import List, Optional

# Profile
class ProfileBase(BaseModel):
    title: str


class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    description: str
    photo_url: str
    poc: str


class Profile(ProfileBase):
    id: int
    owner_id: int
    description: str
    photo_url: str
    phone_number: str
    poc: str

    class Config:
        from_attributes = True

# User
class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    profile: Optional[Profile] = None

    class Config:
        from_attributes = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str
    
# Tag
class TagBase(BaseModel):
    id: int
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    class Config:
        from_attributes = True
        
# Review
class ReviewBase(BaseModel):
    content: str
    rating: int
    
class ReviewCreate(ReviewBase):
    pass

class Review (ReviewBase):
    id: int
    listing_id: int
    profile_id: int
    content: str
    rating: int
    
    class Config:
        from_attributes = True

# JobListing
class JobListingBase(BaseModel):
    title: str
    description: str
    price: float
    
class JobListingCreate(JobListingBase):
    pass
        
class JobListing(JobListingBase):
    id: int
    seller_id: int
    title: str
    description: str
    tags: Optional[List[Tag]]
    reviews: Optional[List[Review]]
    
    class Config:
        # https://pydantic-docs.helpmanual.io/usage/models/#orm-mode-aka-arbitrary-class-instances
        from_attributes = True
        
# Seller
class SellerBase(BaseModel):
    pass
    
class SellerCreate(SellerBase):
    pass

class Seller(SellerBase):
    id: int
    profile_id: int
    rating: int
    jobListings: Optional[List['JobListing']]

    class Config:
        from_attributes = True
            