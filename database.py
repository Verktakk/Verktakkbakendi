from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env.development')
dbpassword = os.getenv('DBPASSWORD')
DATABASE_URL = f"postgresql://maxhgeaz:{dbpassword}@trumpet.db.elephantsql.com/maxhgeaz"
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()