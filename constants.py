import os
from dotenv import load_dotenv

load_dotenv('.env.development')

class AppConfig:
    
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    HASH_ALGORITHM = os.getenv('HASH_ALG')
    TOKEN_EXPIRE_MINUTES: int = 30