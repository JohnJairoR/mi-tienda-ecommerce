from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter()

# =====================================================
# Crear categoría (SIN auth por ahora)
# =====================================================
@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(
        name=category.name,
        slug=category.slug,
        description=category.description,
        image_url=category.image_url
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# =====================================================
# Listar categorías
# =====================================================
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()



