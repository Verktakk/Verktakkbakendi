from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table
from .database import Base

# model = classes and instances that interact with the database

# Creating classes that inherit the Base properties
class User(Base):
    # name of the table to use in the database for each of these models
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    is_active = Column(Boolean, default=True)

   # a "magic" attribute that will contain the values from other tables related to this one.
    profile = relationship("Profile", back_populates="user", 
                           primaryjoin="User.id == Profile.user_id")
    
    # one to one relationship with profile
    
class Profile(Base):
    __tablename__ = 'Profile'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    photo_url = Column(String(255))
    description = Column(String(255))
    phone_number = Column(String)
    poc = Column(String)
    
    seller = relationship("Seller", back_populates="profile", uselist=False) # One-to-One or One-to-Zero with Seller
    review = relationship("Review", uselist=False, back_populates="profile") # Back-reference to Review model
    user = relationship("User", back_populates="profile")  # Back-reference to User model
    
class Seller(Base):
    __tablename__ = 'Seller'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey('Profile.id'))
    rating = Column(Integer)

    # one to one
    profile = relationship("Profile", back_populates="seller")  # Back-reference to Profile model
    job_listings = relationship("JobListing", back_populates="seller")  # One-to-Many relationship with JobListing

    
class Review(Base):
    __tablename__ = 'Review'

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('Seller.id'))
    profile_id = Column(Integer, ForeignKey('Profile.id'))
    listing_id = Column(Integer, ForeignKey('JobListing.id'), unique=True)  # One-to-One relationship with JobListing
    content = Column(String)
    rating = Column(Integer)
    
    
    job_listing = relationship("JobListing", back_populates="review", uselist=False)  # Back-reference to JobListing model
    profile = relationship("Profile", back_populates="review", uselist=False)  # Back-reference to Profile model
    
class JobListing(Base):
    __tablename__ = 'JobListing'
    
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('Seller.id'))
    title = Column(String)
    description = Column(String)
    price = Column(Integer)
    

    seller = relationship("Seller", back_populates="job_listings")  # Back-reference to Seller model
    tags = relationship("Tag", secondary="job_listing_tag_association", back_populates="job_listings")  # Bidirectional relationship with Tag
    review = relationship("Review", uselist=False, back_populates="job_listing") # Back-reference to Review model


class Tag(Base):
    __tablename__ = 'Tag'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    job_listings = relationship("JobListing", secondary="job_listing_tag_association", back_populates="tags")

job_listing_tag_association = Table(
    'job_listing_tag_association',
    Base.metadata,
    Column('job_listing_id', Integer, ForeignKey('JobListing.id')),
    Column('tag_id', Integer, ForeignKey('Tag.id'))
)