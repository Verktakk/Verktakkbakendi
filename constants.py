import os
from dotenv import load_dotenv

load_dotenv('.env.development')

class AppConfig:
    
    DB_PASSWORD = os.getenv('DBPASSWORD')
    SECRET_KEY = os.getenv('SECRET_KEY')
    HASH_ALGORITHM = os.getenv('HASH_ALG')
    TOKEN_EXPIRE_MINUTES: int = 30