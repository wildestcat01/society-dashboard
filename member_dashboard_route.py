from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from db import supabase
from generate_chart_data import generate_payment_chart_data
from datetime import datetime, timedelta
from utils.supabase_client import supabase

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# # Inside member_dashboard_route.py
# @router.get("/member/{user_id}", response_class=HTMLResponse)
# def member_dashboard(request: Request, user_id: str):



#     # Fetch user info (already implemented)
#     user_result = supabase.table("users").select("*").eq("id", user_id).single().execute()
#     user = user_result.data

#     # Fetch payments (already implemented)
#     payments_result = supabase.table("payments").select("*").eq("user_id", user_id).execute()
#     user_payments = payments_result.data if payments_result.data else []

#     # ✅ Fetch latest notice
#     notice_resp = supabase.table("notices").select("*").order("created_at", desc=True).limit(1).execute()
#     notice_text = notice_resp.data[0]["content"] if notice_resp.data else ""

#     months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

#     return templates.TemplateResponse("member_dashboard.html", {
#         "request": request,
#         "user": user,
#         "payments": user_payments,
#         "months": months,
#         "notice_text": notice_text # ✅ make sure this is passed
        
#     })


@router.get("/member/{user_id}")
def member_dashboard(request: Request, user_id: str):
    user_res = supabase.table("users").select("*").eq("id", user_id).single().execute()
    user = user_res.data if user_res.data else {}

    # ✅ Fetch latest notice
    notice_resp = supabase.table("notices").select("*").order("created_at", desc=True).limit(1).execute()
    notice_text = notice_resp.data[0]["content"] if notice_resp.data else ""

    payment_res = supabase.table("payments").select("*").eq("user_id", user_id).execute()
    payments = payment_res.data or []

    enrollment_date = datetime.strptime(user["enrollment_date"], "%Y-%m-%d")
    today = datetime.today()
    current_month_str = today.strftime("%Y-%m")
    last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_month_str = last_month.strftime("%Y-%m")
    start_month = enrollment_date.replace(day=1)
    end_month = (today.replace(day=1) + timedelta(days=62)).replace(day=1)
    

    month_list = []
    current = start_month
    while current <= end_month:
        month_str = current.strftime("%Y-%m")
        paid = any(p["month_paid_for"].startswith(month_str) for p in payments)

        if paid:
            status = "paid"
        elif month_str == current_month_str:
            status = "due"
        elif month_str == last_month_str:
            status = "missed"
        elif current > today:
            status = "upcoming"
        else:
            status = "missed"

        month_list.append({"month": month_str, "status": status})
        current = (current + timedelta(days=32)).replace(day=1)

    next_due = next((m["month"] for m in month_list if m["status"] == "due"), None)
    

    return templates.TemplateResponse("member_dashboard.html", {
        "request": request,
        "user": user,
        "payment_status": month_list,
        "next_due": next_due,
        "due_amount": 500,
        "notice_text": notice_text # ✅ make sure this is passed
    })
