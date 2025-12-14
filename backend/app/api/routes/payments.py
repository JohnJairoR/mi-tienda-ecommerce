from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import stripe
from ...database import get_db
from ...config import settings
from ...api.dependencies import get_current_active_user
from ...models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/payments", tags=["Payments"])

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntentRequest(BaseModel):
    amount: int  # En centavos
    order_id: int


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