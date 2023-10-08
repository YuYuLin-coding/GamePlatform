from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class MemberLevelSchema(BaseModel):
    idx: Optional[int] = None
    member_level: str
    description: Optional[str] = None

class UserSchema(BaseModel):
    user_id: str
    password: Optional[str] = None
    is_active: Optional[bool] = None
    member_level: Optional[str] = None
    user_token: Optional[str] = None

    class Config:
        from_attributes = True # orm_mode 改為 from_attributes

class PermissionSchema(BaseModel):
    permission_name: str
    description: Optional[str] = None
    member_level: Optional[str] = None