from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True
