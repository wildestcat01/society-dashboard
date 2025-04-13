
from fastapi import APIRouter, Request,Form
from fastapi.templating import Jinja2Templates
from utils.supabase_client import supabase
from fastapi.responses import HTMLResponse, RedirectResponse
from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from passlib.hash import bcrypt
from fastapi import APIRouter, Form
from supabase import create_client
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import traceback
import os


router = APIRouter()
templates = Jinja2Templates(directory="templates")



@router.post("/save-notice")
def save_notice(request: Request, content: str = Form(...)):
    supabase.table("notices").insert({"content": content}).execute()
    return RedirectResponse(url="/admin-dashboard", status_code=302)

@router.get("/admin-dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    try:
        now = datetime.now()
        this_month = f"{now.year}-{now.month:02}"
        prev_month = f"{now.year}-{(now.month - 1):02}" if now.month > 1 else f"{now.year - 1}-12"

        members = supabase.table("users").select("*").eq("role", "member").execute().data or []
        payments = supabase.table("payments").select("*").execute().data or []
        expenses = supabase.table("expenses").select("*").order("date").execute().data or []
        notice_result = supabase.table("notices").select("*").order("created_at", desc=True).limit(1).execute()
        notice = notice_result.data[0] if notice_result.data else {"content": ""}

        total_collected = sum([p.get("amount", 0) for p in payments])

        monthly_totals = defaultdict(float)
        for p in payments:
            month = p["month_paid_for"][:7]
            monthly_totals[month] += p["amount"]

        expense_totals = defaultdict(float)
        for exp in expenses:
            month = exp["date"][:7]
            expense_totals[month] += exp["amount"]

        chart_months = sorted(list(set(list(monthly_totals.keys()) + list(expense_totals.keys()))))
        collected_data = [monthly_totals[m] for m in chart_months]
        expense_data = [expense_totals.get(m, 0) for m in chart_months]
        not_paid_data = [0 for _ in chart_months]

        prev_month_balance = monthly_totals.get(prev_month, 0) - expense_totals.get(prev_month, 0)
        current_month_collection = monthly_totals.get(this_month, 0)
        current_month_expenses = expense_totals.get(this_month, 0)
        current_month_balance = current_month_collection - current_month_expenses + prev_month_balance
        paid_map = defaultdict(set)
        for p in payments:
            paid_map[p["user_id"]].add(p["month_paid_for"][:7])

        defaulters = []
        for m in members:
            enrollment = m.get("enrollment_date")
            if not enrollment:
                m["has_due"] = False
                continue
            start = datetime.strptime(enrollment, "%Y-%m-%d")
            check = datetime(start.year, start.month, 1)
            unpaid_months = []
            while check <= now:
                key = f"{check.year}-{check.month:02}"
                if key not in paid_map.get(m["id"], set()):
                    unpaid_months.append(key)
                check += relativedelta(months=1)
            if unpaid_months:
                m["unpaid_months"] = unpaid_months
                m["has_due"] = True
                defaulters.append(m)
            else:
                m["has_due"] = False

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "members": members,
            "payments": payments,
            "expenses": expenses,
            "notice": notice,
            "total_collected": total_collected,
            "chart_months": chart_months,
            "collected_data": collected_data,
            "expense_data": expense_data,
            "not_paid_data": not_paid_data,
            "defaulters": defaulters,
            "prev_month_balance": prev_month_balance,
            "current_month_collection": current_month_collection,
            "current_month_expenses": current_month_expenses,
            "current_month_balance": current_month_balance
        })
    except Exception as e:
        print("[ERROR] Admin dashboard failed:", e)
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "members": [],
            "payments": [],
            "expenses": [],
            "notice": {"content": ""},
            "total_collected": 0,
            "chart_months": [],
            "collected_data": [],
            "expense_data": [],
            "not_paid_data": [],
            "defaulters": [],
            "prev_month_balance": 0,
            "current_month_collection": 0,
            "current_month_expenses": 0,
            "current_month_balance": 0
        })


from fastapi import Form

@router.post("/api/expenses")
def add_expense(
    date: str = Form(...),
    description: str = Form(...),
    amount: float = Form(...)
):
    print("[ADD EXPENSE] Date:", date, "Desc:", description, "Amount:", amount)
    try:
        supabase.table("expenses").insert({
            "date": date,
            "description": description,
            "amount": amount
        }).execute()
        return {"message": "Expense added"}
    except Exception as e:
        print("[ERROR ADDING EXPENSE]", e)
        return {"error": "Could not add expense"}
    
@router.post("/api/members")
def add_member(
    full_name: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    flat_number: str = Form(...),
    vehicle_no: str = Form(""),
    ownership_type: str = Form(...),
    home_locked: str = Form(...),
    password: str = Form(...),
):
    try:
        hashed_password = bcrypt.hash(password)
        alt_phones = []  # Optional: Add alternate_phones if needed
        
        payload = {
            "full_name": full_name,
            "mobile": mobile,
            "email": email,
            "flat_number": flat_number,
            "vehicle_no": vehicle_no,
            "ownership_type": ownership_type,
            "home_locked": home_locked.lower() == "true",  # ensure it's boolean
            "password": bcrypt.hash(password),
            "alternate_phones": [],
            "vehicle_numbers": []
        }

        print("[DEBUG] INSERT PAYLOAD:", payload)

        supabase.table("users").insert(payload).execute()

        return JSONResponse({"success": True, "message": "Member added"})

        # result = supabase.table("members").insert({
        #     "full_name": full_name,
        #     "email": email,
        #     "mobile": mobile,
        #     "flat_number": flat_number,
        #     "vehicle_numbers": [v.strip() for v in vehicle_numbers.split(",") if v.strip()],
        #     "ownership_type": ownership_type,
        #     "home_locked": home_locked == "True",
        #     "password": hashed_password,
        #     "alternate_phones": alt_phones
        # }).execute()

        # return RedirectResponse(url="/admin", status_code=302)

    except Exception as e:
        try:
            error = e.args[0] if isinstance(e.args[0], dict) else {}
            message = error.get("message", "Unknown error")
        except Exception:
            message = "An error occurred while adding the member."

        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": message}
        )
