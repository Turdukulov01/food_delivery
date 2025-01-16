from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from ..database import get_db
from ..models import Order
from ..schemas import OrderCreate, OrderUpdate, OrderResponse
from ..config import get_settings

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)

# Временно отключаем проверку токена
def verify_token(token: str) -> dict:
    return {"sub": "test_user"}

# Временно отключаем отправку уведомлений
def notify_status_change(order_id: int, status: str):
    logger.info(f"Notification would be sent for order {order_id} with status {status}")
    pass

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    try:
        new_order = Order(**order.dict())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        # Отправляем уведомление о новом заказе
        notify_status_change(new_order.id, new_order.status)
        
        return new_order
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return order
    except Exception as e:
        logger.error(f"Error getting order: {e}")
        raise

@router.patch("/{order_id}", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db)
):
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        order.status = order_update.status
        db.commit()
        db.refresh(order)
        
        # Отправляем уведомление об изменении статуса
        notify_status_change(order.id, order.status)
        
        return order
    except Exception as e:
        logger.error(f"Error updating order: {e}")
        raise

@router.get("/", response_model=List[OrderResponse])
def list_orders(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    try:
        orders = db.query(Order).offset(skip).limit(limit).all()
        return orders
    except Exception as e:
        logger.error(f"Error listing orders: {e}")
        raise
