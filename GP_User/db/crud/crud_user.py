from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.models.model_user import DBUser, DBMemberLevel, DBPermission
from schemas.schema_user import UserSchema, MemberLevelSchema, PermissionSchema
from utils.util_security import Hash

def create_user(db: Session, request: UserSchema):
    old_user = db.query(DBUser).filter(DBUser.user_id == request.user_id).first()
    if old_user:
        raise HTTPException(status_code=400, detail="User already registered")
    new_user = DBUser(
        user_id = request.user_id,
        password_hash = Hash.hash_password(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, user_id: str, password: str):
    user = db.query(DBUser).filter(DBUser.user_id == user_id, DBUser.is_active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User ID is not found or not active.'
        )
    if not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'User ID or Password is not correct.'
        )
    return user

def update_user(db: Session, request: UserSchema):
    user = db.query(DBUser).filter(DBUser.user_id == request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User ID is not found'
        )
    user.is_active = request.is_active
    user.member_level = request.member_level

def delete_user(db: Session, user_id: str):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User ID is not found'
        )
    db.delete(user)
    db.commit()