from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import stripe
import mercadopago
import os
from app.database import get_db
from app.config import settings
from app.api.dependencies import get_current_active_user
from app.models.user import User
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any

router = APIRouter(prefix="/payments", tags=["Payments"])

# ===== CONFIGURACIÓN DE STRIPE =====
stripe.api_key = settings.STRIPE_SECRET_KEY

# ===== CONFIGURACIÓN DE MERCADO PAGO =====
MERCADOPAGO_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN")

if MERCADOPAGO_ACCESS_TOKEN:
    sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
else:
    print("⚠️ MERCADOPAGO_ACCESS_TOKEN no configurado")
    sdk = None


# ===== MODELOS PARA STRIPE =====

class CreatePaymentIntentRequest(BaseModel):
    amount: int  # En centavos
    order_id: int


# ===== MODELOS PARA MERCADO PAGO =====

class MercadoPagoItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    picture_url: Optional[str] = None
    category_id: str = "others"
    quantity: int
    unit_price: float
    currency_id: str = "PEN"  # PEN, USD, ARS, MXN, etc.


class PayerPhone(BaseModel):
    area_code: str
    number: str


class PayerIdentification(BaseModel):
    type: str
    number: str


class PayerAddress(BaseModel):
    street_name: str
    street_number: Optional[str] = ""
    zip_code: Optional[str] = ""


class Payer(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: PayerPhone
    identification: PayerIdentification
    address: PayerAddress


class BackUrls(BaseModel):
    success: str
    failure: str
    pending: str


class PreferenceRequest(BaseModel):
    items: List[MercadoPagoItem]
    payer: Payer
    back_urls: BackUrls
    auto_return: str = "approved"
    payment_methods: Optional[Dict[str, Any]] = None
    notification_url: Optional[str] = None
    statement_descriptor: Optional[str] = "MI TIENDA"
    external_reference: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# ===== ENDPOINTS DE STRIPE =====

@router.post("/create-intent")
def create_payment_intent(
        request: CreatePaymentIntentRequest,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Crear payment intent de Stripe"""
    try:
        intent = stripe.PaymentIntent.create(
            amount=request.amount,
            currency="usd",
            metadata={
                "order_id": request.order_id,
                "user_id": current_user.id
            }
        )

        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===== ENDPOINTS DE MERCADO PAGO =====

@router.post("/create-preference")
async def create_preference(preference_data: PreferenceRequest):
    """
    Crea una preferencia de pago en Mercado Pago
    No requiere autenticación para permitir compras como invitado
    """
    if not sdk:
        raise HTTPException(
            status_code=503,
            detail="Mercado Pago no está configurado. Contacta al administrador."
        )

    try:
        # Preparar datos para Mercado Pago
        preference_dict = {
            "items": [item.dict() for item in preference_data.items],
            "payer": preference_data.payer.dict(),
            "back_urls": preference_data.back_urls.dict(),
            "auto_return": preference_data.auto_return,
        }

        # Agregar campos opcionales si existen
        if preference_data.payment_methods:
            preference_dict["payment_methods"] = preference_data.payment_methods

        if preference_data.notification_url:
            preference_dict["notification_url"] = preference_data.notification_url

        if preference_data.statement_descriptor:
            preference_dict["statement_descriptor"] = preference_data.statement_descriptor

        if preference_data.external_reference:
            preference_dict["external_reference"] = preference_data.external_reference

        if preference_data.metadata:
            preference_dict["metadata"] = preference_data.metadata

        print("📦 Creando preferencia en Mercado Pago...")

        # Crear preferencia en Mercado Pago
        preference_response = sdk.preference().create(preference_dict)

        print(f"📊 Respuesta de MP: Status {preference_response['status']}")

        if preference_response["status"] == 201:
            return {
                "id": preference_response["response"]["id"],
                "init_point": preference_response["response"]["init_point"],
                "sandbox_init_point": preference_response["response"]["sandbox_init_point"],
            }
        else:
            print(f"❌ Error en respuesta: {preference_response}")
            raise HTTPException(
                status_code=400,
                detail=f"Error al crear preferencia en Mercado Pago"
            )

    except Exception as e:
        print(f"❌ Error en create_preference: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el pago: {str(e)}"
        )


@router.post("/webhooks/mercadopago")
async def mercadopago_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Webhook para recibir notificaciones de Mercado Pago
    Documentación: https://www.mercadopago.com.pe/developers/es/docs/your-integrations/notifications/webhooks
    """
    try:
        # Obtener datos del webhook
        body = await request.json()

        print("📩 Webhook recibido de Mercado Pago:", body)

        # Verificar el tipo de notificación
        notification_type = body.get("type")

        if notification_type == "payment":
            payment_id = body.get("data", {}).get("id")

            if payment_id and sdk:
                # Obtener información del pago
                payment_info = sdk.payment().get(payment_id)

                if payment_info["status"] == 200:
                    payment = payment_info["response"]

                    print(f"💰 Pago ID: {payment_id}")
                    print(f"📊 Estado: {payment.get('status')}")
                    print(f"💵 Monto: {payment.get('transaction_amount')}")
                    print(f"📧 Email: {payment.get('payer', {}).get('email')}")

                    # Obtener referencia externa (ID de orden)
                    status = payment.get("status")
                    external_reference = payment.get("external_reference")

                    # TODO: Actualizar orden en tu base de datos
                    # Estados posibles:
                    # - approved: Pago aprobado
                    # - pending: Pago pendiente
                    # - rejected: Pago rechazado
                    # - refunded: Pago reembolsado
                    # - cancelled: Pago cancelado

                    """
                    Ejemplo de actualización de orden:

                    if external_reference:
                        order = db.query(Order).filter(
                            Order.external_reference == external_reference
                        ).first()

                        if order:
                            if status == "approved":
                                order.status = "paid"
                                order.payment_id = payment_id
                            elif status == "rejected":
                                order.status = "payment_failed"

                            db.commit()
                    """

                    return {"status": "ok", "message": "Webhook procesado"}

        return {"status": "ok", "message": "Notificación recibida"}

    except Exception as e:
        print(f"❌ Error en webhook: {str(e)}")
        # Siempre devolver 200 para que Mercado Pago no reintente
        return {"status": "error", "message": str(e)}


@router.get("/payment/{payment_id}")
async def get_payment_info(payment_id: str):
    """
    Obtiene información de un pago específico de Mercado Pago
    """
    if not sdk:
        raise HTTPException(
            status_code=503,
            detail="Mercado Pago no está configurado"
        )

    try:
        payment_info = sdk.payment().get(payment_id)

        if payment_info["status"] == 200:
            return payment_info["response"]
        else:
            raise HTTPException(
                status_code=404,
                detail="Pago no encontrado"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener información del pago: {str(e)}"
        )


# ===== ENDPOINT PARA OBTENER MÉTODOS DE PAGO DISPONIBLES =====

@router.get("/methods")
async def get_payment_methods():
    """
    Retorna los métodos de pago disponibles en la tienda
    """
    methods = []

    # Verificar si Stripe está configurado
    if stripe.api_key:
        methods.append({
            "id": "stripe",
            "name": "Stripe",
            "description": "Tarjetas de crédito/débito internacionales",
            "available": True
        })

    # Verificar si Mercado Pago está configurado
    if sdk:
        methods.append({
            "id": "mercadopago",
            "name": "Mercado Pago",
            "description": "Tarjetas, Yape, Plin y más métodos locales",
            "available": True
        })

    # Métodos alternativos (siempre disponibles)
    methods.extend([
        {
            "id": "yape",
            "name": "Yape / Plin",
            "description": "Pago móvil instantáneo",
            "available": True
        },
        {
            "id": "transferencia",
            "name": "Transferencia Bancaria",
            "description": "Depósito o transferencia directa",
            "available": True
        }
    ])

    return {
        "methods": methods,
        "total": len(methods)
    }


# ===== INSTRUCCIONES DE CONFIGURACIÓN =====
"""
📋 CONFIGURACIÓN DE MERCADO PAGO:

1. Instalar dependencia:
   pip install mercadopago

2. Obtener credenciales:
   - Ve a: https://www.mercadopago.com.pe/developers
   - Crea una aplicación
   - Copia tu Access Token

3. Agregar a .env:
   MERCADOPAGO_ACCESS_TOKEN=TEST-1234567890-121212-abc...

4. Configurar webhook en Mercado Pago:
   - Dashboard > Tu aplicación > Webhooks
   - URL: https://tu-api.com/api/payments/webhooks/mercadopago
   - Eventos: Pagos

5. Tarjetas de prueba:
   Aprobada:
   - Número: 5031 7557 3453 0604
   - CVV: 123
   - Fecha: 11/25

   Rechazada:
   - Número: 5031 4332 1540 6351
   - CVV: 123
   - Fecha: 11/25

📋 AMBOS PROCESADORES:
Este archivo soporta tanto Stripe como Mercado Pago.
Solo configura las variables de entorno del que quieras usar.
"""