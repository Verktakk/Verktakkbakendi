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
    phone_number = Column(String, unique=True, index=True)

   # a "magic" attribute that will contain the values from other tables related to this one.
    profile = relationship("Profile", back_populates="user", 
                           uselist=False,
                           passive_deletes=True)
    
    # one to one relationship with profile
    
class Profile(Base):
    __tablename__ = 'Profile'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'))
    photo_url = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    poc = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    seller = relationship("Seller", back_populates="profile", uselist=False, passive_deletes=True) # One-to-One or One-to-Zero with Seller
    review = relationship("Review", back_populates="profile", passive_deletes=True) # Back-reference to Review model
    user = relationship("User", back_populates="profile", uselist=False)  # Back-reference to User model
    
class Seller(Base):
    __tablename__ = 'Seller'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey('Profile.id', ondelete='CASCADE'))
    rating = Column(Integer)

    # one to one
    profile = relationship("Profile", back_populates="seller", uselist=False)  # Back-reference to Profile model
    job_listings = relationship("JobListing", back_populates="seller", passive_deletes=True)  # One-to-Many relationship with JobListing

    
class Review(Base):
    __tablename__ = 'Review'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('Profile.id'))
    listing_id = Column(Integer, ForeignKey('JobListing.id', ondelete='CASCADE'), unique=True)  # One-to-One relationship with JobListing
    content = Column(String)
    rating = Column(Integer)
    
    
    job_listing = relationship("JobListing", back_populates="review", uselist=False, passive_deletes=True)  # Back-reference to JobListing model
    profile = relationship("Profile", back_populates="review", uselist=False)  # Back-reference to Profile model
    
class JobListing(Base):
    __tablename__ = 'JobListing'
    
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('Seller.id', ondelete='CASCADE'))
    title = Column(String)
    description = Column(String)
    price = Column(Integer)
    

    seller = relationship("Seller", back_populates="job_listings", uselist=False)  # Back-reference to Seller model
    tags = relationship("Tag", secondary="job_listing_tag_association", back_populates="job_listings")  # Bidirectional relationship with Tag
    review = relationship("Review", back_populates="job_listing", passive_deletes=True) # Back-reference to Review model


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