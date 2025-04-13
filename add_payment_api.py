
from fastapi import APIRouter, Form
from utils.supabase_client import supabase
from datetime import datetime



router = APIRouter()

@router.post("/api/payments")
def add_payment(
    user_id: str = Form(...),
    month_paid_for: str = Form(...),
    amount: float = Form(...),
    payment_mode: str = Form(...)
):
    payment_data = {
        "user_id": user_id,
        "month_paid_for": f"{month_paid_for}-01",
        "amount": amount,
        "payment_mode": payment_mode,
        "payment_date": datetime.utcnow().isoformat()
    }
    try:
        supabase.table("payments").insert(payment_data).execute()
        return {"status": "success", "message": "Payment recorded"}
    except Exception as e:
        print("[ERROR] Failed to add payment:", e)
        return {"status": "error", "message": "Failed to add payment"}
    
