import uuid
from sqlalchemy import Column, BigInteger, SmallInteger, String, Text, Numeric, Boolean, DateTime, ForeignKey, ARRAY, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.models.base import Base

class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(BigInteger, primary_key=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    restaurant_dish_id = Column(BigInteger, ForeignKey('restaurant_dish.restaurant_dish_id'), nullable=False)
    rating = Column(SmallInteger, nullable=False)
    text = Column(Text)
    sentiment_score = Column(Numeric(4, 3))
    tags = Column(ARRAY(Text))
    photo_urls = Column(ARRAY(Text))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(BigInteger, primary_key=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    review_id = Column(BigInteger, ForeignKey('reviews.review_id'), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Like(Base):
    __tablename__ = 'likes'

    like_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    review_id = Column(BigInteger, ForeignKey('reviews.review_id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'review_id', name='uq_user_review_like'),
    )
