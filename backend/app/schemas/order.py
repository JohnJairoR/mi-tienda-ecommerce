from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from ..models.order import OrderStatus


# Schema para item de orden
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    price: float


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_sku: Optional[str] = None
    quantity: int
    price: float
    subtotal: float

    class Config:
        from_attributes = True


# Schema para crear orden
class OrderCreate(BaseModel):
    shipping_name: str = Field(..., min_length=1)
    shipping_email: EmailStr
    shipping_phone: Optional[str] = None
    shipping_address: str = Field(..., min_length=1)
    shipping_city: str = Field(..., min_length=1)
    shipping_state: Optional[str] = None
    shipping_zip: Optional[str] = None
    shipping_country: str = Field(..., min_length=1)
    notes: Optional[str] = None
    items: List[OrderItemCreate]


# Schema para respuesta de orden
class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: int
    shipping_name: str
    shipping_email: str
    shipping_phone: Optional[str] = None
    shipping_address: str
    shipping_city: str
    shipping_state: Optional[str] = None
    shipping_zip: Optional[str] = None
    shipping_country: str
    subtotal: float
    shipping_cost: float
    tax: float
    total: float
    status: OrderStatus
    payment_method: Optional[str] = None
    payment_id: Optional[str] = None
    paid_at: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


# Schema para actualizar orden
class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_id: Optional[str] = None
    notes: Optional[str] = None