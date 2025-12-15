import requests

# Configuración
API_BASE = "https://mi-tienda-ecommerce.onrender.com/api"
USERNAME = "admin@tienda.com"
PASSWORD = "123456"

def login():
    """Hacer login y obtener token"""
    print("🔐 Iniciando sesión...")
    response = requests.post(
        f"{API_BASE}/auth/login",
        data={
            "username": USERNAME,
            "password": PASSWORD
        }
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login exitoso")
        return token
    else:
        print(f"❌ Error en login: {response.text}")
        return None

def crear_categorias(token):
    """Crear categorías"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    categorias = [
        {"name": "Tecnología", "slug": "tecnologia"},
        {"name": "Ropa y Moda", "slug": "ropa-moda"},
        {"name": "Hogar", "slug": "hogar"},
        {"name": "Deportes", "slug": "deportes"},
        {"name": "Libros", "slug": "libros"},
    ]
    print("\n📦 Creando categorías...")
    for cat in categorias:
        res = requests.post(f"{API_BASE}/categories/", json=cat, headers=headers)
        if res.status_code == 201:
            print(f"✅ Categoría creada: {cat['name']}")
        elif res.status_code == 400 and "already exists" in res.text:
            print(f"⚠️ La categoría ya existe: {cat['name']}")
        else:
            print(f"❌ Error al crear {cat['name']}: {res.status_code} {res.text}")

def crear_productos(token):
    """Crear productos"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    productos = [
        # Tecnología
        {"name": "iPhone 15 Pro Max", "slug": "iphone-15-pro-max", "description": "El smartphone más avanzado con chip A17 Pro", "price": 1299.99, "category_id": 1, "image_url": "https://images.unsplash.com/photo-1592286927505-5c2c2f8a1f85?w=500"},
        {"name": "MacBook Pro M3", "slug": "macbook-pro-m3", "description": "Laptop profesional con chip M3 y pantalla Retina", "price": 2499.99, "category_id": 1, "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500"},
        {"name": "AirPods Pro", "slug": "airpods-pro", "description": "Auriculares inalámbricos con cancelación de ruido", "price": 249.99, "category_id": 1, "image_url": "https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=500"},
        {"name": "iPad Air", "slug": "ipad-air", "description": "Tablet versátil con chip M1", "price": 599.99, "category_id": 1, "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500"},
        {"name": "Apple Watch Series 9", "slug": "apple-watch-9", "description": "Smartwatch con monitor de salud avanzado", "price": 399.99, "category_id": 1, "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=500"},
        # Ropa y Moda
        {"name": "Chaqueta de Cuero", "slug": "chaqueta-cuero", "description": "Chaqueta de cuero genuino estilo biker", "price": 299.99, "category_id": 2, "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500"},
        {"name": "Zapatillas Nike Air Max", "slug": "nike-air-max", "description": "Zapatillas deportivas con tecnología Air", "price": 159.99, "category_id": 2, "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"},
        {"name": "Jeans Levi's 501", "slug": "levis-501", "description": "Jeans clásicos de corte regular", "price": 89.99, "category_id": 2, "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500"},
        {"name": "Reloj Casio G-Shock", "slug": "casio-gshock", "description": "Reloj resistente al agua y golpes", "price": 129.99, "category_id": 2, "image_url": "https://images.unsplash.com/photo-1587836374615-91d3f9b6f7f0?w=500"},
        {"name": "Gafas de Sol Ray-Ban", "slug": "rayban-aviator", "description": "Gafas de sol estilo aviador clásico", "price": 179.99, "category_id": 2, "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500"},
        # Hogar
        {"name": "Cafetera Nespresso", "slug": "nespresso-vertuo", "description": "Cafetera de cápsulas automática", "price": 199.99, "category_id": 3, "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500"},
        {"name": "Aspiradora Dyson V15", "slug": "dyson-v15", "description": "Aspiradora inalámbrica con tecnología láser", "price": 649.99, "category_id": 3, "image_url": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=500"},
        {"name": "Licuadora Vitamix", "slug": "vitamix-pro", "description": "Licuadora profesional de alta potencia", "price": 449.99, "category_id": 3, "image_url": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=500"},
        {"name": "Lámpara LED Inteligente", "slug": "lampara-led-smart", "description": "Lámpara con control por app y cambio de color", "price": 49.99, "category_id": 3, "image_url": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=500"},
        {"name": "Sartén Antiadherente", "slug": "sarten-tefal", "description": "Sartén de 28cm con recubrimiento antiadherente", "price": 39.99, "category_id": 3, "image_url": "https://images.unsplash.com/photo-1556910110-a5a63dfd393c?w=500"},
        # Deportes
        {"name": "Bicicleta de Montaña Trek", "slug": "trek-mountain-bike", "description": "Bicicleta MTB con suspensión completa", "price": 1299.99, "category_id": 4, "image_url": "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?w=500"},
        {"name": "Mancuernas Ajustables", "slug": "mancuernas-20kg", "description": "Set de mancuernas de 2-20kg ajustables", "price": 199.99, "category_id": 4, "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500"},
        {"name": "Yoga Mat Premium", "slug": "yoga-mat-premium", "description": "Tapete de yoga antideslizante 6mm", "price": 39.99, "category_id": 4, "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500"},
        {"name": "Pelota de Fútbol Nike", "slug": "balon-futbol-nike", "description": "Balón oficial tamaño 5", "price": 29.99, "category_id": 4, "image_url": "https://images.unsplash.com/photo-1614632537190-23e4146777db?w=500"},
        {"name": "Raqueta de Tenis Wilson", "slug": "raqueta-wilson", "description": "Raqueta profesional de grafito", "price": 179.99, "category_id": 4, "image_url": "https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=500"},
        # Libros
        {"name": "Sapiens - Yuval Noah Harari", "slug": "sapiens-harari", "description": "De animales a dioses: Breve historia de la humanidad", "price": 24.99, "category_id": 5, "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500"},
        {"name": "El Señor de los Anillos", "slug": "lotr-trilogia", "description": "Trilogía completa edición especial", "price": 49.99, "category_id": 5, "image_url": "https://images.unsplash.com/photo-1621351183012-e2f9972dd9bf?w=500"},
        {"name": "Atomic Habits", "slug": "atomic-habits", "description": "Un método fácil y comprobado para crear buenos hábitos", "price": 19.99, "category_id": 5, "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500"},
        {"name": "1984 - George Orwell", "slug": "1984-orwell", "description": "Novela distópica clásica", "price": 14.99, "category_id": 5, "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=500"},
        {"name": "Clean Code", "slug": "clean-code", "description": "Manual de desarrollo ágil de software", "price": 39.99, "category_id": 5, "image_url": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=500"},
        # Extras
        {"name": "PlayStation 5", "slug": "playstation-5", "description": "Consola de videojuegos de nueva generación", "price": 499.99, "category_id": 1, "image_url": "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=500"},
        {"name": "Mochila North Face", "slug": "mochila-northface", "description": "Mochila de trekking 40L", "price": 129.99, "category_id": 2, "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"},
        {"name": "Freidora de Aire", "slug": "freidora-aire", "description": "Freidora sin aceite 5.5L", "price": 99.99, "category_id": 3, "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"},
        {"name": "Cuerda para Saltar", "slug": "cuerda-saltar", "description": "Cuerda de velocidad ajustable", "price": 19.99, "category_id": 4, "image_url": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500"},
        {"name": "Harry Potter Colección", "slug": "harry-potter-set", "description": "Serie completa de 7 libros", "price": 89.99, "category_id": 5, "image_url": "https://images.unsplash.com/photo-1621351183012-e2f9972dd9bf?w=500"}
    ]

    print(f"\n📦 Creando {len(productos)} productos...")
    exitosos = 0
    errores = 0

    for producto in productos:
        res = requests.post(f"{API_BASE}/products/", json=producto, headers=headers)
        if res.status_code == 201:
            print(f"✅ {producto['name']}")
            exitosos += 1
        else:
            print(f"❌ Error en {producto['name']}: {res.status_code} {res.text}")
            errores += 1

    print(f"\n✨ Resumen: ✅ {exitosos} | ❌ {errores} | Total {len(productos)}")

if __name__ == "__main__":
    print("🚀 Iniciando script de categorías y productos...")

    token = login()
    if token:
        crear_categorias(token)
        crear_productos(token)
        print("\n✅ ¡Proceso completado!")
    else:
        print("\n❌ No se pudo iniciar sesión")


