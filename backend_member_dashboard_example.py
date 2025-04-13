
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from utils.supabase_client import supabase

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/member/{user_id}")
def member_dashboard(request: Request, user_id: str):
    # Fetch user info
    user_res = supabase.table("users").select("*").eq("id", user_id).single().execute()
    user = user_res.data if user_res.data else {}

    # Fetch all payments by this user
    payment_res = supabase.table("payments").select("*").eq("user_id", user_id).execute()
    payments = payment_res.data or []

    # Determine payment months from enrollment to current + 2 future
    enrollment_date = datetime.strptime(user["enrollment_date"], "%Y-%m-%d")
    today = datetime.today()
    start_month = enrollment_date.replace(day=1)
    end_month = (today.replace(day=1) + timedelta(days=62)).replace(day=1)

    month_list = []
    current = start_month
    while current <= end_month:
        month_str = current.strftime("%Y-%m")
        paid = any(p["month_paid_for"].startswith(month_str) for p in payments)
        status = "paid" if paid else "due" if current < today else "upcoming"
        month_list.append({"month": month_str, "status": status})
        current = (current + timedelta(days=32)).replace(day=1)

    # Detect next due payment
    next_due = next((m["month"] for m in month_list if m["status"] == "due"), None)

    return templates.TemplateResponse("member_dashboard.html", {
        "request": request,
        "user": user,
        "payment_status": month_list,
        "next_due": next_due,
        "due_amount": 500,
    })
