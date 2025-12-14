from .api.routes import payments_router  # This import is fine up top
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from .api.routes import (
    auth_router,
    products_router,
    cart_router,
    orders_router
)

# --- CORRECTED ORDER: Define the 'app' instance first ---

# Crear aplicación FastAPI
app = FastAPI(
    title="Mi Tienda API",
    description="API REST para tienda e-commerce profesional",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- Now we can use 'app' to register middleware and routers ---

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas (including the new payments_router)
app.include_router(auth_router, prefix="/api")
app.include_router(products_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(payments_router, prefix="/api") # Integrated successfully here

# Crear tablas en la base de datos
# Note: This is typically done at startup or via migrations, but it works here too.
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    """Endpoint raíz"""
    return {
        "message": "Bienvenido a Mi Tienda API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
