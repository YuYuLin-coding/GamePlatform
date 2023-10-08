from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from config import Config
from db.database import get_db
from db.crud.crud_user import get_user

SECRET_KEY = "SecretKey"
ALGORITHM = 'HS256'
JWT_ACCESS_TOKEN_EXPIRES_DAYS = Config.JWT_ACCESS_TOKEN_EXPIRES_DAYS
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=JWT_ACCESS_TOKEN_EXPIRES_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception()
    
    except JWTError:
        raise credentials_exception
    user = get_user(db, user_id)
    if user is None:
        raise credentials_exception()
    return user