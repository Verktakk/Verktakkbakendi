from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import psycopg2
import os
from dotenv import load_dotenv

from constants import AppConfig

DATABASE_URL = f"postgresql://maxhgeaz:{AppConfig.DB_PASSWORD}@trumpet.db.elephantsql.com/maxhgeaz"
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

# Each instance of the SessonLocal class will be a db session
# See main.py where we inistialize a db session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  Later we will inherit from this Base to create each of the database models or classes
Base = declarative_base()