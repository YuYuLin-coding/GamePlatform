from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.oauth2 import create_access_token
from db.database import get_db
from db.models.model_user import DBUser
from utils.util_security import Hash

router = APIRouter(
    tags=['auth']
)
@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(DBUser).filter(DBUser.user_id == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials or incorrect password")
    if not user.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials or incorrect password")
    access_token = create_access_token(data={'user_id': user.user_id, 'member_level': user.member_level})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.user_id,
        'member_level': user.member_level
    }