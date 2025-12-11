import bcrypt
from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()

# Verificar si ya existe
existing = db.query(User).filter(User.username == "admin").first()

if existing:
    print("⚠️ Usuario admin ya existe")
    print(f"   Email: {existing.email}")
    print(f"   Es admin: {existing.is_admin}")
else:
    # Crear hash de la contraseña
    password = "admin123"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    admin = User(
        email="admin@mitienda.com",
        username="admin",
        full_name="Administrador",
        hashed_password=hashed.decode('utf-8'),
        is_active=True,
        is_admin=True
    )
    db.add(admin)
    db.commit()
    print("✅ Usuario admin creado exitosamente")
    print("   Username: admin")
    print("   Password: admin123")

db.close()