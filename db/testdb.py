from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from constants import AppConfig
from .models import User, Profile
from .database import Base


DATABASE_URL = f"postgresql://maxhgeaz:{AppConfig.DB_PASSWORD}@trumpet.db.elephantsql.com/maxhgeaz"
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Create a session maker
Session = sessionmaker(bind=engine)

# Create a new user
session = Session()

