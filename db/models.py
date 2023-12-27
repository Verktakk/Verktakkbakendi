from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# model = classes and instances that interact with the database

# Creating classes that inherit the Base properties
class User(Base):
    # name of the table to use in the database for each of these models
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    is_active = Column(Boolean, default=True)

    # a "magic" attribute that will contain the values from other tables related to this one.
    items = relationship("Profile", back_populates="owner", primaryjoin="User.id == Profile.user_id")
    
class Profile(Base):
    __tablename__ = 'Profile'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    photo_url = Column(String(255))
    description = Column(String(255))
    phone_number = Column(String)
    poc = Column(String)
    # seller_id = Column(Integer, ForeignKey('Seller.id'))
    # review_ids = 
    
    owner = relationship("User", back_populates="items")
    

