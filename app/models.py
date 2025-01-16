from sqlalchemy import Column, Integer, String, Float, ARRAY, DateTime, ForeignKey, Enum
import enum
from datetime import datetime
from .database import Base

class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    PREPARING = "PREPARING"
    DELIVERING = "DELIVERING"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False)
    restaurant_id = Column(Integer, nullable=False)
    items = Column(ARRAY(Integer), nullable=False)  # Array of item IDs
    total_price = Column(Float, nullable=False)
    delivery_address = Column(String, nullable=False)
    status = Column(String, default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
