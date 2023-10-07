from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class MemberLevelSchema(BaseModel):
    idx: int
    member_level: str
    description: str
    
    class Config:
        from_attributes = True # orm 改為 from_attributes

class UserSchema(BaseModel):
    user_id: str
    password: Optional[str]
    is_active: Optional[bool]
    member_level: MemberLevelSchema  # 表達 User 與 MemberLevel 的關聯
    user_token: Optional[str]

    class Config:
        from_attributes = True

class PermissionSchema(BaseModel):
    permission_name: str
    description: Optional[str]
    
    class Config:
        from_attributes = True