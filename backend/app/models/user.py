import uuid
from sqlalchemy import Column, BigInteger, String, Text, Boolean, JSON, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.models.base import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    bio = Column(Text)
    avatar_url = Column(Text)
    city = Column(String(100))
    taste_profile = Column(JSON)
    is_verified = Column(Boolean, default=False)
    role = Column(String(50), default="user") # anonymous, user, restaurant_owner, moderator, admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Follower(Base):
    __tablename__ = 'followers'

    follow_id = Column(BigInteger, primary_key=True, autoincrement=True)
    follower_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    following_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='uq_follower_following'),
    )
