import uuid
from sqlalchemy import Column, BigInteger, String, Text, Numeric, Boolean, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.models.base import Base

class Restaurant(Base):
    __tablename__ = 'restaurants'

    restaurant_id = Column(BigInteger, primary_key=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    lat = Column(Numeric(9, 6), nullable=False)
    lng = Column(Numeric(9, 6), nullable=False)
    cuisine_tags = Column(ARRAY(Text))
    avg_rating = Column(Numeric(3, 2))
    created_by = Column(BigInteger, ForeignKey('users.user_id'))
    approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
