from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Información de envío
    shipping_name = Column(String, nullable=False)
    shipping_email = Column(String, nullable=False)
    shipping_phone = Column(String, nullable=True)
    shipping_address = Column(Text, nullable=False)
    shipping_city = Column(String, nullable=False)
    shipping_state = Column(String, nullable=True)
    shipping_zip = Column(String, nullable=True)
    shipping_country = Column(String, nullable=False)

    # Montos
    subtotal = Column(Float, nullable=False)
    shipping_cost = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    total = Column(Float, nullable=False)

    # Estado y pago
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_method = Column(String, nullable=True)
    payment_id = Column(String, nullable=True)  # Stripe payment intent ID
    paid_at = Column(DateTime, nullable=True)

    # Notas
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    product_name = Column(String, nullable=False)  # Guardar nombre por si se borra el producto
    product_sku = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Precio al momento de la compra
    subtotal = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
