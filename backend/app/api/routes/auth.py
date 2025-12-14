from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ...database import get_db
from ...schemas.user import UserCreate, UserResponse, Token
from ...services.auth_service import (
    create_user,
    authenticate_user,
    get_user_by_username,
    get_user_by_email
)
from ...utils.security import create_access_token
from ...config import settings
from ...api.dependencies import get_current_active_user
from ...models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


# =========================
# REGISTRO
# =========================
@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar username
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username ya registrado")

    # Verificar email
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email ya registrado")

    new_user = create_user(db, user)

    access_token = create_access_token(
        data={"sub": new_user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user
    }


# =========================
# LOGIN
# =========================
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


# =========================
# USUARIO ACTUAL
# =========================
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# ==========================================================
# 🔐 ENDPOINT TEMPORAL PARA HACER ADMIN (BORRAR DESPUÉS)
# ==========================================================
@router.post("/make-admin")
def make_admin(
    email: str,
    db: Session = Depends(get_db)
):
    """
    ⚠️ USAR SOLO UNA VEZ Y LUEGO BORRAR
    """
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.is_admin = True
    db.commit()

    return {
        "message": f"Usuario {user.email} ahora es ADMIN"
    }

