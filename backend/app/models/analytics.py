import uuid
from sqlalchemy import Column, BigInteger, String, Numeric, Integer, Date, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.models.base import Base

class CustomerFeature(Base):
    __tablename__ = 'customer_features'

    feature_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False, unique=True)
    visit_count = Column(Integer, default=0)
    days_since_last_visit = Column(Integer, default=0)
    avg_rating_given = Column(Numeric(3, 2))
    avg_sentiment = Column(Numeric(4, 3))
    bookmark_activity = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class CustomerSegment(Base):
    __tablename__ = 'customer_segments'

    segment_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False, unique=True)
    segment_name = Column(String(50), nullable=False) # e.g. at_risk, loyal, new
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ChurnPrediction(Base):
    __tablename__ = 'churn_predictions'

    prediction_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False, unique=True)
    churn_probability = Column(Numeric(4, 3), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class RestaurantDailyMetric(Base):
    __tablename__ = 'restaurant_daily_metrics'

    metric_id = Column(BigInteger, primary_key=True, autoincrement=True)
    restaurant_id = Column(BigInteger, ForeignKey('restaurants.restaurant_id'), nullable=False)
    date = Column(Date, nullable=False)
    avg_rating = Column(Numeric(3, 2))
    positive_sentiment_pct = Column(Numeric(5, 4))
    churn_rate = Column(Numeric(5, 4))
    review_velocity = Column(Integer)
    health_score = Column(Numeric(5, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BusinessReport(Base):
    __tablename__ = 'business_reports'

    report_id = Column(BigInteger, primary_key=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    restaurant_id = Column(BigInteger, ForeignKey('restaurants.restaurant_id'), nullable=False)
    report_type = Column(String(50), nullable=False) # e.g. PDF, CSV
    s3_path = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
