from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database import get_db
from ...models.cart import CartItem
from ...models.product import Product
from ...models.user import User
from ...schemas.cart import CartItemCreate, CartItemUpdate, CartItemResponse, CartResponse
from ...api.dependencies import get_current_active_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=CartResponse)
def get_cart(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Obtener carrito del usuario actual"""
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()

    subtotal = sum(item.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    return {
        "items": cart_items,
        "subtotal": subtotal,
        "total_items": total_items
    }


@router.post("/", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
        item: CartItemCreate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Agregar producto al carrito"""
    # Verificar que el producto existe
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    # Verificar stock
    if product.stock < item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock insuficiente. Solo hay {product.stock} unidades disponibles"
        )

    # Verificar si el producto ya está en el carrito
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == item.product_id
    ).first()

    if existing_item:
        # Actualizar cantidad
        existing_item.quantity += item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    # Crear nuevo item
    cart_item = CartItem(
        user_id=current_user.id,
        product_id=item.product_id,
        quantity=item.quantity,
        price=product.price
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.put("/{item_id}", response_model=CartItemResponse)
def update_cart_item(
        item_id: int,
        item: CartItemUpdate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Actualizar cantidad de un item del carrito"""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado en el carrito"
        )

    # Verificar stock
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if product.stock < item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock insuficiente. Solo hay {product.stock} unidades disponibles"
        )

    cart_item.quantity = item.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
        item_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Eliminar item del carrito"""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado en el carrito"
        )

    db.delete(cart_item)
    db.commit()
    return None


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Vaciar todo el carrito"""
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    return None
