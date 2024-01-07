from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db import schemas
from app.db import models
from app.db import crud
from constants import AppConfig

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                       create_user_request: schemas.UserCreate):
    user = models.User(
        email=create_user_request.email,
        name=create_user_request.name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
    )
    logging.error(user)
    db.add(user)
    db.commit()

    # except Exception as e:
    #     # Log the error or handle it in a way that makes sense for your application
    #     logging.error(e)
    #     # You might want to rollback the database session in case of an error
    #     db.rollback()
    #     # Raise an HTTPException with a 500 Internal Server Error status code
    #     raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication failed')
    token = create_access_token(user.email, user.id, timedelta(minutes=AppConfig.TOKEN_EXPIRE_MINUTES))
    return {'access_token': token, 'token_type': 'bearer'}
    

def authenticate_user(email: str, password: str, db):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, AppConfig.SECRET_KEY, algorithm=AppConfig.HASH_ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, AppConfig.SECRET_KEY, algorithms=[AppConfig.HASH_ALGORITHM])
        email: str = payload.get('sub')
        user_id: int = payload.get('id')
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validate user')
        return {'email': email, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='could not validate user')
        
