from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, UniqueConstraint, ForeignKeyConstraint, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from db.database import Base
from utils.util_security import Hash

@dataclass
class DBUser(Base):
    __tablename__ = "users"

    idx: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: str = Column(String(50), unique=True, nullable=False)
    password_hash: str = Column(String(200), nullable=False)
    is_active: bool = Column(Boolean, default=True)
    member_level_id = Column(Integer, ForeignKey('member_level.idx'))  # 添加外鍵關聯
    login_attempts: int = Column(Integer, default=0)
    last_login_attempt: datetime = Column(DateTime, default=None)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow,
                                  server_default=text('CURRENT_TIMESTAMP'))
    updated_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow,
                                  server_default=text('CURRENT_TIMESTAMP'), onupdate=datetime.utcnow)

    # Assuming we have a foreign key to the member level
    member_level_id: int = Column(Integer, ForeignKey('member_levels.idx'))

    member_level = relationship("DBMemberLevel", back_populates="users")

    def verify_password(self, password: str):
        return Hash.verify_password(password, self.password_hash)

    def update_password(self, password: str):
        self.password_hash = Hash.hash_password(password)


# 多對多關聯表設定

member_level_permissions = Table(
    'member_level_permissions',
    Base.metadata,
    Column('member_level_id', Integer, ForeignKey('member_levels.idx'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.idx'), primary_key=True)
)

@dataclass
class DBMemberLevel(Base):
    __tablename__ = "member_levels"

    idx: int = Column(Integer, primary_key=True, autoincrement=True)
    member_level: str = Column(String(50), unique=True, nullable=False)
    description: str = Column(String(200), nullable=True)

    users = relationship("DBUser", back_populates="member_level")
    permissions = relationship("DBPermission", secondary=member_level_permissions, back_populates="member_levels")


@dataclass
class DBPermission(Base):
    __tablename__ = "permissions"

    idx: int = Column(Integer, primary_key=True, autoincrement=True)
    permission_name: str = Column(String(50), unique=True, nullable=False)
    description: str = Column(String(200), nullable=True)

    member_levels = relationship("DBMemberLevel", secondary=member_level_permissions, back_populates="permissions")