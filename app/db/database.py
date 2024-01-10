from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import psycopg2

from constants import AppConfig

engine = create_engine(AppConfig.DATABASE_URL, connect_args={"sslmode": "require"})

# Each instance of the SessonLocal class will be a db session
# See main.py where we inistialize a db session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  Later we will inherit from this Base to create each of the database models or classes
Base = declarative_base()

def init_db():
    print("models created!")
    # Create the database tables
    Base.metadata.create_all(bind=engine)

