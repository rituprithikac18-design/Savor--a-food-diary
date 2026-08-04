import uuid
from sqlalchemy import Column, BigInteger, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.models.base import Base

class List(Base):
    __tablename__ = 'lists'

    list_id = Column(BigInteger, primary_key=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Bookmark(Base):
    __tablename__ = 'bookmarks'

    bookmark_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    restaurant_dish_id = Column(BigInteger, ForeignKey('restaurant_dish.restaurant_dish_id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'restaurant_dish_id', name='uq_user_bookmark'),
    )

class Notification(Base):
    __tablename__ = 'notifications'

    notification_id = Column(BigInteger, primary_key=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
