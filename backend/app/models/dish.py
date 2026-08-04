import uuid
from sqlalchemy import Column, BigInteger, String, Text, Numeric, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.models.base import Base

class Dish(Base):
    __tablename__ = 'dishes'

    dish_id = Column(BigInteger, primary_key=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    embedding_vector = Column(Vector(384))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RestaurantDish(Base):
    __tablename__ = 'restaurant_dish'

    restaurant_dish_id = Column(BigInteger, primary_key=True, autoincrement=True)
    restaurant_id = Column(BigInteger, ForeignKey('restaurants.restaurant_id'), nullable=False)
    dish_id = Column(BigInteger, ForeignKey('dishes.dish_id'), nullable=False)
    price = Column(Numeric(8, 2))
    love_count = Column(Integer, default=0)
    avg_rating = Column(Numeric(3, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
