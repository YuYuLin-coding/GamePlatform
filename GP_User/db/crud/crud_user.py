from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.models.model_user import DBUser, DBMembergroup, DBPermission
from schemas.schema_user import UserSchema, MemberLevelSchema, PermissionSchema
from utils.util_security import Hash

def create_user(db: Session, request: UserSchema):
    old_user = db.query(DBUser).filter(DBUser.user_id == request.user_id).first()
    if old_user:
        raise HTTPException(status_code=400, detail="User already registered")
    new_user = DBUser(
        user_id = request.user_id,
        password_hash = Hash.hash_password(request.password),
        member_level = request.member_level
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
    if user.login_attempts > 3 and datetime.utcnow() - user.last_login_attempt < timedelta(minutes=1):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Wrong password > 3 times, wait 1 min.'
        )
    user.last_login_attempt = datetime.utcnow()
    
    if not user.verify_password(password):
        user.login_attempts = user.login_attempts + 1
        
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'User password is not correct.'
        )
    user.login_attempts = 0
    db.commit()
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

def get_user(db: Session, user_id: str):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User ID: {user_id} is not found.'
        )
    return user

def create_member_level(db: Session, request: MemberLevelSchema):
    member = db.query(DBMembergroup).filter(DBMembergroup.member_level == request.member_level).first()
    if member:
        raise HTTPException(status_code=400, detail="Member already registered")
    new_member = DBMembergroup(
        member_level = request.member_level,
        description = request.description
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def delete_member_level(db: Session, member_level: str):
    member = db.query(DBMembergroup).filter(DBMembergroup.member_level == member_level).first()
    if not member:
        raise HTTPException(status_code=400, detail="Member is not found")
    db.delete(member)
    db.commit()
    return f'Member {member_level} is deleted successfully.'