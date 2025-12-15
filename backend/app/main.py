from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.payments import router as payments_router
from app.api.routes.categories import router as categories_router  # ✅ AÑADIDO
from .config import settings
from .database import engine, Base
from .api.routes import (
    auth_router,
    products_router,
    cart_router,
    orders_router
)

# =========================================================
# Crear aplicación FastAPI
# =========================================================

app = FastAPI(
    title="Mi Tienda API",
    description="API REST para tienda e-commerce profesional",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mi-tienda-ecommerce.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# Registrar rutas
# =========================================================

app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(products_router, prefix="/api", tags=["Products"])
app.include_router(categories_router, prefix="/api/categories", tags=["Categories"])  # ✅ AQUÍ
app.include_router(cart_router, prefix="/api", tags=["Cart"])
app.include_router(orders_router, prefix="/api", tags=["Orders"])
app.include_router(payments_router, prefix="/api", tags=["Payments"])

# =========================================================
# Base de datos
# =========================================================

Base.metadata.create_all(bind=engine)

# =========================================================
# Endpoints base
# =========================================================

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a Mi Tienda API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }

# =========================================================
# Run local
# =========================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )


