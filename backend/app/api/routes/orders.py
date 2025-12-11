from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import secrets
from ...database import get_db
from ...models.order import Order, OrderItem, OrderStatus
from ...models.product import Product
from ...models.cart import CartItem
from ...models.user import User
from ...schemas.order import OrderCreate, OrderResponse, OrderUpdate
from ...api.dependencies import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/orders", tags=["Orders"])


def generate_order_number() -> str:
    """Generar número de orden único"""
    timestamp = datetime.now().strftime("%Y%m%d")
    random_part = secrets.token_hex(4).upper()
    return f"ORD-{timestamp}-{random_part}"


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
        order_data: OrderCreate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Crear nueva orden desde el carrito o items específicos"""
    # Validar que hay items
    if not order_data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La orden debe tener al menos un producto"
        )

    # Calcular totales
    subtotal = 0
    order_items = []

    for item_data in order_data.items:
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto {item_data.product_id} no encontrado"
            )

        # Verificar stock
        if product.stock < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para {product.name}"
            )

        item_subtotal = item_data.price * item_data.quantity
        subtotal += item_subtotal

        order_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "product_sku": product.sku,
            "quantity": item_data.quantity,
            "price": item_data.price,
            "subtotal": item_subtotal
        })

    # Calcular shipping y tax (puedes personalizarlo)
    shipping_cost = 0.0 if subtotal > 50 else 10.0
    tax = subtotal * 0.0  # 0% impuesto (ajustar según tu país)
    total = subtotal + shipping_cost + tax

    # Crear orden
    order = Order(
        order_number=generate_order_number(),
        user_id=current_user.id,
        shipping_name=order_data.shipping_name,
        shipping_email=order_data.shipping_email,
        shipping_phone=order_data.shipping_phone,
        shipping_address=order_data.shipping_address,
        shipping_city=order_data.shipping_city,
        shipping_state=order_data.shipping_state,
        shipping_zip=order_data.shipping_zip,
        shipping_country=order_data.shipping_country,
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        tax=tax,
        total=total,
        notes=order_data.notes,
        status=OrderStatus.PENDING
    )

    db.add(order)
    db.flush()  # Para obtener el ID de la orden

    # Crear items de la orden
    for item_data in order_items:
        order_item = OrderItem(
            order_id=order.id,
            **item_data
        )
        db.add(order_item)

        # Reducir stock
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        product.stock -= item_data["quantity"]

    # Limpiar carrito del usuario
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()

    db.commit()
    db.refresh(order)

    return order


@router.get("/", response_model=List[OrderResponse])
def get_my_orders(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Obtener órdenes del usuario actual"""
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
        order_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Obtener detalle de una orden"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada"
        )

    # Verificar que la orden pertenece al usuario (excepto si es admin)
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta orden"
        )

    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
        order_id: int,
        order_update: OrderUpdate,
        current_user: User = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
):
    """Actualizar orden (solo admin)"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada"
        )

    # Actualizar campos
    update_data = order_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)

    # Si se marca como pagada, actualizar fecha
    if order_update.status == OrderStatus.PAID and not order.paid_at:
        order.paid_at = datetime.utcnow()

    db.commit()
    db.refresh(order)
    return order
