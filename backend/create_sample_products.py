import requests

API_BASE = "https://mi-tienda-ecommerce.onrender.com/api"
USERNAME = "admin@tienda.com"
PASSWORD = "123456"


def login():
    print("🔐 Iniciando sesión...")
    r = requests.post(
        f"{API_BASE}/auth/login",
        data={"username": USERNAME, "password": PASSWORD}
    )
    r.raise_for_status()
    print("✅ Login exitoso")
    return r.json()["access_token"]


def crear_productos(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    productos = [
        # 🔌 TECNOLOGÍA (1)
        {
            "name": "iPhone 15 Pro Max",
            "slug": "iphone-15-pro-max",
            "description": "Smartphone Apple con pantalla de 6.7 pulgadas, chip A17 Pro y cámara de 48MP",
            "price": 1299.99,
            "stock": 50,
            "category_id": 1,
            "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500"
        },
        {
            "name": "MacBook Pro M3",
            "slug": "macbook-pro-m3",
            "description": "Laptop profesional con chip M3, 16GB RAM y pantalla Retina",
            "price": 2499.99,
            "stock": 30,
            "category_id": 1,
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500"
        },
        {
            "name": "AirPods Pro",
            "slug": "airpods-pro",
            "description": "Auriculares inalámbricos con cancelación de ruido activa",
            "price": 249.99,
            "stock": 100,
            "category_id": 1,
            "image_url": "https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=500"
        },
        {
            "name": "iPad Air",
            "slug": "ipad-air",
            "description": "Tablet Apple con pantalla de 10.9 pulgadas y chip M1",
            "price": 599.99,
            "stock": 45,
            "category_id": 1,
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500"
        },
        {
            "name": "Apple Watch Series 9",
            "slug": "apple-watch-9",
            "description": "Smartwatch con monitoreo de salud y GPS integrado",
            "price": 399.99,
            "stock": 60,
            "category_id": 1,
            "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=500"
        },

        # 👕 ROPA Y MODA (2)
        {
            "name": "Chaqueta de Cuero",
            "slug": "chaqueta-cuero",
            "description": "Chaqueta estilo biker de cuero genuino",
            "price": 299.99,
            "stock": 25,
            "category_id": 2,
            "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500"
        },
        {
            "name": "Zapatillas Nike Air Max",
            "slug": "nike-air-max",
            "description": "Zapatillas deportivas con amortiguación Air",
            "price": 159.99,
            "stock": 80,
            "category_id": 2,
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"
        },
        {
            "name": "Jeans Levi's 501",
            "slug": "levis-501",
            "description": "Jeans clásicos de corte recto",
            "price": 89.99,
            "stock": 120,
            "category_id": 2,
            "image_url": "https://images.unsplash.com/photo-1542272454315-7f6fabf313a3?w=500"
        },
        {
            "name": "Reloj Casio G-Shock",
            "slug": "casio-gshock",
            "description": "Reloj resistente al agua y golpes",
            "price": 129.99,
            "stock": 40,
            "category_id": 2,
            "image_url": "https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e?w=500"
        },
        {
            "name": "Gafas Ray-Ban",
            "slug": "rayban",
            "description": "Gafas de sol clásicas con protección UV",
            "price": 179.99,
            "stock": 55,
            "category_id": 2,
            "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500"
        },

        # 🏠 HOGAR (3)
        {
            "name": "Cafetera Nespresso",
            "slug": "cafetera-nespresso",
            "description": "Cafetera de cápsulas con sistema de presión",
            "price": 199.99,
            "stock": 35,
            "category_id": 3,
            "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500"
        },
        {
            "name": "Aspiradora Dyson",
            "slug": "dyson-v15",
            "description": "Aspiradora sin cable con detección de partículas",
            "price": 649.99,
            "stock": 20,
            "category_id": 3,
            "image_url": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=500"
        },
        {
            "name": "Licuadora Vitamix",
            "slug": "vitamix",
            "description": "Licuadora profesional de alta potencia",
            "price": 449.99,
            "stock": 28,
            "category_id": 3,
            "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"
        },
        {
            "name": "Lámpara LED",
            "slug": "lampara-led",
            "description": "Lámpara inteligente con control por app",
            "price": 49.99,
            "stock": 90,
            "category_id": 3,
            "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500"
        },
        {
            "name": "Sartén Antiadherente",
            "slug": "sarten",
            "description": "Sartén profesional de 28cm",
            "price": 39.99,
            "stock": 75,
            "category_id": 3,
            "image_url": "https://images.unsplash.com/photo-1556909172-54557c7e4fb7?w=500"
        },

        # 🏀 DEPORTES (4)
        {
            "name": "Bicicleta Trek",
            "slug": "bicicleta-trek",
            "description": "Bicicleta de montaña con suspensión completa",
            "price": 1299.99,
            "stock": 15,
            "category_id": 4,
            "image_url": "https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=500"
        },
        {
            "name": "Mancuernas Ajustables",
            "slug": "mancuernas",
            "description": "Set de mancuernas de 5 a 25 kg",
            "price": 199.99,
            "stock": 42,
            "category_id": 4,
            "image_url": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=500"
        },
        {
            "name": "Yoga Mat",
            "slug": "yoga-mat",
            "description": "Tapete antideslizante para yoga y pilates",
            "price": 39.99,
            "stock": 110,
            "category_id": 4,
            "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500"
        },
        {
            "name": "Pelota Nike",
            "slug": "balon-nike",
            "description": "Balón de fútbol tamaño oficial",
            "price": 29.99,
            "stock": 85,
            "category_id": 4,
            "image_url": "https://images.unsplash.com/photo-1614632537423-1e6c2e7e0aab?w=500"
        },
        {
            "name": "Raqueta Wilson",
            "slug": "raqueta-wilson",
            "description": "Raqueta de tenis profesional",
            "price": 179.99,
            "stock": 32,
            "category_id": 4,
            "image_url": "https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=500"
        },

        # 📚 LIBROS (5)
        {
            "name": "Sapiens",
            "slug": "sapiens",
            "description": "De animales a dioses - Yuval Noah Harari",
            "price": 19.99,
            "stock": 150,
            "category_id": 5,
            "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500"
        },
        {
            "name": "El Señor de los Anillos",
            "slug": "lotr",
            "description": "Trilogía completa de fantasía épica - J.R.R. Tolkien",
            "price": 29.99,
            "stock": 95,
            "category_id": 5,
            "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500"
        },
        {
            "name": "Atomic Habits",
            "slug": "atomic-habits",
            "description": "Cómo crear buenos hábitos - James Clear",
            "price": 18.99,
            "stock": 200,
            "category_id": 5,
            "image_url": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=500"
        },
        {
            "name": "1984",
            "slug": "1984",
            "description": "Novela distópica - George Orwell",
            "price": 14.99,
            "stock": 180,
            "category_id": 5,
            "image_url": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=500"
        },
        {
            "name": "Clean Code",
            "slug": "clean-code",
            "description": "Manual de desarrollo ágil de software - Robert C. Martin",
            "price": 39.99,
            "stock": 65,
            "category_id": 5,
            "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500"
        },
    ]

    print("\n📦 Creando productos...")
    ok, fail = 0, 0

    for p in productos:
        r = requests.post(f"{API_BASE}/products/", json=p, headers=headers)
        if r.status_code in (200, 201):
            print(f"✅ {p['name']}")
            ok += 1
        else:
            print(f"❌ {p['name']} -> {r.text}")
            fail += 1

    print("\n✨ RESUMEN")
    print(f"✅ Exitosos: {ok}")
    print(f"❌ Errores: {fail}")


if __name__ == "__main__":
    token = login()
    crear_productos(token)
