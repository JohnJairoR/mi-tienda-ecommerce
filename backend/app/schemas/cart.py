from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Schema para agregar al carrito
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


# Schema para actualizar cantidad
class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


# Schema para respuesta de item del carrito
class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Schema para carrito completo
class CartResponse(BaseModel):
    items: list[CartItemResponse]
    subtotal: float
    total_items: int
