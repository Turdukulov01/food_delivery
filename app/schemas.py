from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import OrderStatus

class OrderBase(BaseModel):
    customer_id: int
    restaurant_id: int
    items: List[int]  # Список ID товаров
    total_price: float
    delivery_address: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(OrderBase):
    id: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    detail: str
