from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv('.env.development')
dbpassword = os.getenv('DBPASSWORD')
SQLALCHEMY_DATABASE_URL = "postgres://maxhgeaz:"+ dbpassword +"@trumpet.db.elephantsql.com/maxhgeaz"
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()