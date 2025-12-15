from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.api.deps import get_current_admin_user

router = APIRouter()

@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    # Verificar si ya existe
    exists = db.query(Category).filter(Category.slug == category.slug).first()
    if exists:
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


