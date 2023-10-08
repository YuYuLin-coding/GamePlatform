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
    member_level = Column(String(50), ForeignKey('member_group.member_level'), nullable=False)  # 添加外鍵關聯
    login_attempts: int = Column(Integer, default=0)
    last_login_attempt: datetime = Column(DateTime, default=None)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow,
                                  server_default=text('CURRENT_TIMESTAMP'))
    updated_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow,
                                  server_default=text('CURRENT_TIMESTAMP'), onupdate=datetime.utcnow)

    member_group = relationship("DBMembergroup", back_populates="users")

    def verify_password(self, password: str):
        return Hash.verify_password(password, self.password_hash)

    def update_password(self, password: str):
        self.password_hash = Hash.hash_password(password)

@dataclass
class DBMembergroup(Base):
    __tablename__ = "member_group"

    idx: int = Column(Integer, primary_key=True, autoincrement=True)
    member_level: str = Column(String(50), unique=True, nullable=False)
    description: str = Column(String(200))

    users = relationship("DBUser", back_populates="member_group")
    permissions = relationship("DBPermission", back_populates="member_group")


@dataclass
class DBPermission(Base):
    __tablename__ = "permissions"

    idx: int = Column(Integer, primary_key=True, autoincrement=True)
    permission_name: str = Column(String(200), nullable=False)
    permission_action: str = Column(String(200), index=True, nullable=False)
    permission_enable: bool = Column(Boolean, default=False)
    description: str = Column(String(200), nullable=True)
    member_level: str = Column(String(50), ForeignKey('member_group.member_level'))

    member_group = relationship("DBMembergroup", back_populates="permissions")

    __table_args__ = (
        UniqueConstraint('member_level', 'permission_action', name='uq_group_permission'),
        ForeignKeyConstraint(['member_level'], ['member_group.member_level'])  # Add foreign key constraint
    )