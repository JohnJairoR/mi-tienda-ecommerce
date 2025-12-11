from app.database import SessionLocal
from app.models.product import Product
from app.models.category import Category

db = SessionLocal()

print("🏪 Creando categorías y productos de ejemplo...")
print("=" * 60)

# Crear categorías
categories_data = [
    {"name": "Electrónica", "slug": "electronica", "description": "Dispositivos y gadgets tecnológicos"},
    {"name": "Ropa", "slug": "ropa", "description": "Moda y vestimenta"},
    {"name": "Hogar", "slug": "hogar", "description": "Artículos para el hogar"},
    {"name": "Deportes", "slug": "deportes", "description": "Equipamiento deportivo"},
    {"name": "Libros", "slug": "libros", "description": "Libros y literatura"},
]

categories = {}
for cat_data in categories_data:
    existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
    if existing:
        categories[cat_data["slug"]] = existing
        print(f"✓ Categoría '{cat_data['name']}' ya existe")
    else:
        category = Category(**cat_data)
        db.add(category)
        db.flush()
        categories[cat_data["slug"]] = category
        print(f"✅ Categoría '{cat_data['name']}' creada")

db.commit()

print("\n📦 Creando productos...")
print("=" * 60)

# Crear productos
products_data = [
    # Electrónica
    {
        "name": "Laptop HP Pavilion 15",
        "slug": "laptop-hp-pavilion-15",
        "description": "Laptop potente con procesador Intel Core i7, 16GB RAM, 512GB SSD",
        "price": 899.99,
        "compare_price": 1099.99,
        "stock": 15,
        "sku": "LAP-HP-001",
        "category_id": categories["electronica"].id,
        "is_featured": True,
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500"
    },
    {
        "name": "iPhone 15 Pro",
        "slug": "iphone-15-pro",
        "description": "El último iPhone con chip A17 Pro y cámara de 48MP",
        "price": 1199.99,
        "compare_price": 1299.99,
        "stock": 25,
        "sku": "PHO-IP-001",
        "category_id": categories["electronica"].id,
        "is_featured": True,
        "image_url": "https://images.unsplash.com/photo-1592286927505-5c2c2f8a1f85?w=500"
    },
    {
        "name": "Auriculares Sony WH-1000XM5",
        "slug": "auriculares-sony-wh1000xm5",
        "description": "Auriculares con cancelación de ruido premium",
        "price": 349.99,
        "stock": 30,
        "sku": "AUD-SON-001",
        "category_id": categories["electronica"].id,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"
    },
    {
        "name": "Tablet Samsung Galaxy Tab S9",
        "slug": "tablet-samsung-galaxy-s9",
        "description": "Tablet Android de 11 pulgadas con S Pen incluido",
        "price": 649.99,
        "stock": 20,
        "sku": "TAB-SAM-001",
        "category_id": categories["electronica"].id,
        "image_url": "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=500"
    },

    # Ropa
    {
        "name": "Camiseta Básica Negra",
        "slug": "camiseta-basica-negra",
        "description": "Camiseta 100% algodón, corte regular",
        "price": 19.99,
        "compare_price": 29.99,
        "stock": 100,
        "sku": "CAM-BAS-001",
        "category_id": categories["ropa"].id,
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500"
    },
    {
        "name": "Jeans Levi's 501",
        "slug": "jeans-levis-501",
        "description": "Jeans clásicos de corte recto",
        "price": 89.99,
        "stock": 50,
        "sku": "JEA-LEV-001",
        "category_id": categories["ropa"].id,
        "is_featured": True,
        "image_url": "https://images.unsplash.com/photo-1542272454315-7f6d6a9a9d8f?w=500"
    },
    {
        "name": "Zapatillas Nike Air Max",
        "slug": "zapatillas-nike-air-max",
        "description": "Zapatillas deportivas con tecnología Air",
        "price": 129.99,
        "stock": 40,
        "sku": "ZAP-NIK-001",
        "category_id": categories["ropa"].id,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"
    },

    # Hogar
    {
        "name": "Cafetera Nespresso",
        "slug": "cafetera-nespresso",
        "description": "Cafetera de cápsulas automática",
        "price": 199.99,
        "stock": 25,
        "sku": "CAF-NES-001",
        "category_id": categories["hogar"].id,
        "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500"
    },
    {
        "name": "Aspiradora Dyson V15",
        "slug": "aspiradora-dyson-v15",
        "description": "Aspiradora inalámbrica con tecnología láser",
        "price": 599.99,
        "compare_price": 699.99,
        "stock": 15,
        "sku": "ASP-DYS-001",
        "category_id": categories["hogar"].id,
        "is_featured": True,
        "image_url": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=500"
    },
    {
        "name": "Lámpara LED Inteligente",
        "slug": "lampara-led-inteligente",
        "description": "Lámpara con control por app y cambio de color",
        "price": 49.99,
        "stock": 60,
        "sku": "LAM-LED-001",
        "category_id": categories["hogar"].id,
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500"
    },

    # Deportes
    {
        "name": "Bicicleta de Montaña",
        "slug": "bicicleta-montana",
        "description": "Bicicleta MTB con suspensión completa",
        "price": 799.99,
        "stock": 10,
        "sku": "BIC-MTB-001",
        "category_id": categories["deportes"].id,
        "image_url": "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?w=500"
    },
    {
        "name": "Mancuernas Ajustables 20kg",
        "slug": "mancuernas-ajustables-20kg",
        "description": "Set de mancuernas con peso ajustable",
        "price": 149.99,
        "stock": 35,
        "sku": "MAN-ADJ-001",
        "category_id": categories["deportes"].id,
        "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500"
    },

    # Libros
    {
        "name": "El Señor de los Anillos - Trilogía",
        "slug": "senor-anillos-trilogia",
        "description": "Edición especial de la trilogía completa",
        "price": 49.99,
        "stock": 45,
        "sku": "LIB-LOTR-001",
        "category_id": categories["libros"].id,
        "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500"
    },
    {
        "name": "Sapiens - Yuval Noah Harari",
        "slug": "sapiens-yuval-harari",
        "description": "De animales a dioses: Breve historia de la humanidad",
        "price": 24.99,
        "stock": 50,
        "sku": "LIB-SAP-001",
        "category_id": categories["libros"].id,
        "is_featured": True,
        "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500"
    },
]

for prod_data in products_data:
    existing = db.query(Product).filter(Product.slug == prod_data["slug"]).first()
    if existing:
        print(f"  ⚠️  '{prod_data['name']}' ya existe")
    else:
        product = Product(**prod_data)
        db.add(product)
        featured = "⭐" if prod_data.get("is_featured") else "  "
        print(f"  ✅ {featured} '{prod_data['name']}' - ${prod_data['price']}")

db.commit()

print("\n" + "=" * 60)
print("✨ ¡Productos creados exitosamente!")
print(f"📊 Total de productos: {db.query(Product).count()}")
print(f"📂 Total de categorías: {db.query(Category).count()}")
print("=" * 60)

db.close()