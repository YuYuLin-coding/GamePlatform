from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db.crud import crud_user
from db.database import get_db
from schemas import schema_user

router = APIRouter(
    prefix='/api/user',
    tags=['api_user']
)

@router.post("/", response_model=schema_user.UserSchema)
def create_user(user: schema_user.UserSchema, db: Session = Depends(get_db)):
    new_user = crud_user.create_user(db, request=user)
    
    return new_user

@router.put("/{user_id}", response_model=schema_user.UserSchema)
def update_user(user_id: int, user: schema_user.UserSchema, db: Session = Depends(get_db)):
    user = crud_user.update_user(db, user=user)
    return 

@router.post("/login")
def login(user: schema_user.UserSchema, db: Session = Depends(get_db)):
    db_user = crud_user.login_user(db, user_id=user.user_id, password=user.password)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud_user.delete_user(db, user_id=user_id)
    return "User: {} delete successfully".format(user_id)