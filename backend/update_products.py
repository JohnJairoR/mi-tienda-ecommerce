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


def obtener_productos(token):
    """Obtiene todos los productos existentes"""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{API_BASE}/products/", headers=headers)
    r.raise_for_status()
    data = r.json()

    # Debug: ver qué estructura tiene la respuesta
    print(f"\n🔍 Estructura de respuesta: {type(data)}")
    if isinstance(data, dict):
        print(f"   Claves disponibles: {list(data.keys())}")

    return data


def actualizar_productos(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Datos actualizados con imágenes y stock
    productos_data = {
        # 🔌 TECNOLOGÍA
        "iphone-15-pro-max": {
            "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500",
            "stock": 50
        },
        "macbook-pro-m3": {
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500",
            "stock": 30
        },
        "airpods-pro": {
            "image_url": "https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=500",
            "stock": 100
        },
        "ipad-air": {
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500",
            "stock": 45
        },
        "apple-watch-9": {
            "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=500",
            "stock": 60
        },

        # 👕 ROPA Y MODA
        "chaqueta-cuero": {
            "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500",
            "stock": 25
        },
        "nike-air-max": {
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500",
            "stock": 80
        },
        "levis-501": {
            "image_url": "https://images.unsplash.com/photo-1542272454315-7f6fabf313a3?w=500",
            "stock": 120
        },
        "casio-gshock": {
            "image_url": "https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e?w=500",
            "stock": 40
        },
        "rayban": {
            "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500",
            "stock": 55
        },

        # 🏠 HOGAR
        "cafetera-nespresso": {
            "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500",
            "stock": 35
        },
        "dyson-v15": {
            "image_url": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=500",
            "stock": 20
        },
        "vitamix": {
            "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=500",
            "stock": 28
        },
        "lampara-led": {
            "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500",
            "stock": 90
        },
        "sarten": {
            "image_url": "https://images.unsplash.com/photo-1556909172-54557c7e4fb7?w=500",
            "stock": 75
        },

        # 🏀 DEPORTES
        "bicicleta-trek": {
            "image_url": "https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=500",
            "stock": 15
        },
        "mancuernas": {
            "image_url": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=500",
            "stock": 42
        },
        "yoga-mat": {
            "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500",
            "stock": 110
        },
        "balon-nike": {
            "image_url": "https://images.unsplash.com/photo-1614632537423-1e6c2e7e0aab?w=500",
            "stock": 85
        },
        "raqueta-wilson": {
            "image_url": "https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=500",
            "stock": 32
        },

        # 📚 LIBROS
        "sapiens": {
            "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500",
            "stock": 150
        },
        "lotr": {
            "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
            "stock": 95
        },
        "atomic-habits": {
            "image_url": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=500",
            "stock": 200
        },
        "1984": {
            "image_url": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=500",
            "stock": 180
        },
        "clean-code": {
            "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500",
            "stock": 65
        },
    }

    # Obtener productos existentes
    print("\n📋 Obteniendo productos existentes...")
    response_data = obtener_productos(token)

    # Manejar diferentes formatos de respuesta
    if isinstance(response_data, dict):
        # Si es un diccionario, buscar la lista de productos
        productos = response_data.get('products', response_data.get('items', response_data.get('data', [])))
    elif isinstance(response_data, list):
        productos = response_data
    else:
        print(f"❌ Formato de respuesta no reconocido: {type(response_data)}")
        return

    print(f"✅ Se encontraron {len(productos)} productos")

    if len(productos) > 0:
        print(f"\n📝 Ejemplo de producto: {productos[0]}")

    print("\n🔄 Actualizando productos...")

    ok, fail, skip = 0, 0, 0

    for producto in productos:
        try:
            # Asegurarnos de que el producto es un diccionario
            if isinstance(producto, str):
                print(f"⚠️  Producto es string, no diccionario: {producto}")
                skip += 1
                continue

            slug = producto.get("slug")
            product_id = producto.get("id")

            if not slug or not product_id:
                print(f"⚠️  Producto sin slug o id: {producto}")
                skip += 1
                continue

            if slug in productos_data:
                # Preparar datos de actualización
                update_data = {
                    "name": producto["name"],
                    "slug": producto["slug"],
                    "description": producto["description"],
                    "price": producto["price"],
                    "category_id": producto["category_id"],
                    "image_url": productos_data[slug]["image_url"],
                    "stock": productos_data[slug]["stock"]
                }

                # Actualizar producto
                r = requests.put(
                    f"{API_BASE}/products/{product_id}",
                    json=update_data,
                    headers=headers
                )

                if r.status_code in (200, 201):
                    print(f"✅ {producto['name']} - Stock: {update_data['stock']}")
                    ok += 1
                else:
                    print(f"❌ {producto['name']} -> {r.status_code}: {r.text}")
                    fail += 1
            else:
                print(f"⚠️  {producto.get('name', 'Desconocido')} (slug: {slug}) - No hay datos para actualizar")
                skip += 1

        except Exception as e:
            print(f"❌ Error procesando producto: {e}")
            print(f"   Producto: {producto}")
            fail += 1

    print("\n✨ RESUMEN")
    print(f"✅ Actualizados: {ok}")
    print(f"❌ Errores: {fail}")
    print(f"⏭️  Omitidos: {skip}")


if __name__ == "__main__":
    token = login()
    actualizar_productos(token)