from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Schema para crear producto
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    compare_price: Optional[float] = Field(None, gt=0)
    cost_price: Optional[float] = Field(None, gt=0)
    stock: int = Field(default=0, ge=0)
    sku: Optional[str] = None
    barcode: Optional[str] = None
    is_active: bool = True
    is_featured: bool = False
    weight: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    images: Optional[str] = None  # JSON string
    category_id: Optional[int] = None


# Schema para actualizar producto
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    compare_price: Optional[float] = Field(None, gt=0)
    cost_price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    sku: Optional[str] = None
    barcode: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    weight: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    images: Optional[str] = None
    category_id: Optional[int] = None


# Schema para respuesta de producto
class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    price: float
    compare_price: Optional[float] = None
    cost_price: Optional[float] = None
    stock: int
    sku: Optional[str] = None
    barcode: Optional[str] = None
    is_active: bool
    is_featured: bool
    weight: Optional[float] = None
    image_url: Optional[str] = None
    images: Optional[str] = None
    category_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Schema para listado de productos
class ProductList(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    pages: int
