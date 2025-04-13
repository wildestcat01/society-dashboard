
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client
from passlib.hash import bcrypt
from member_search_route import router as search_router
from admin_routes import router as admin_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from notice_routes import router as notice_router
from fastapi.staticfiles import StaticFiles
from auth_routes import router as auth_router
from member_dashboard_route import router as member_dashboard_router
from dotenv import load_dotenv
load_dotenv()
from utils.supabase_client import supabase
from member_actions import router as member_action_router
from defaulters_export_route import router as defaulters_router
from export_defaulters_csv import router as export_defaulters_router
from add_payment_api import router as payment_router
from starlette.middleware.sessions import SessionMiddleware
from auth_routes import router as auth_router
from fastapi import APIRouter, Form
from passlib.hash import bcrypt
from passlib.hash import bcrypt

import os

app = FastAPI()
app.include_router(admin_router)
app.include_router(auth_router)
templates = Jinja2Templates(directory="templates")
app.include_router(member_dashboard_router)
app.include_router(search_router)
app.add_middleware(SessionMiddleware, secret_key="society-key")
app.include_router(notice_router)
app.include_router(member_action_router)
app.include_router(defaulters_router)
app.include_router(export_defaulters_router)
app.include_router(payment_router)
app.add_middleware(SessionMiddleware, secret_key="your-secret")
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Admin Dashboard API running!"}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, mobile: str = Form(...), password: str = Form(...)):
    result = supabase.table("users").select("*").eq("mobile", mobile).execute()
    if not result.data:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    user = result.data[0]
    if not bcrypt.verify(password, user["password"]):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    """ if user.get("role") == "admin":
        return RedirectResponse(url=f"/admin/{user['id']}", status_code=status.HTTP_302_FOUND) """
    if user.get("role") == "admin":
       return RedirectResponse(url="/admin-dashboard", status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url=f"/member/{user['id']}", status_code=status.HTTP_302_FOUND)

import json

def parse_vehicle_numbers(vehicle_numbers):
    if isinstance(vehicle_numbers, list):
        return [v.strip() for v in vehicle_numbers if v.strip()]
    elif isinstance(vehicle_numbers, str):
        # Try to parse if it's a JSON string
        try:
            parsed = json.loads(vehicle_numbers)
            if isinstance(parsed, list):
                return [v.strip() for v in parsed if isinstance(v, str) and v.strip()]
        except Exception:
            # If not JSON, fall back to comma split
            return [v.strip() for v in vehicle_numbers.split(",") if v.strip()]
    return []

@app.post("/update-profile")
def update_profile(
    request: Request,
    user_id: str = Form(...),
    flat_number: str = Form(...),
    email: str = Form(...),
    alternate_phones: str = Form(...),
    vehicle_numbers: str = Form(...),
    home_locked: bool = Form(False),
    ownership_type: str = Form(...)
):
    print("[UPDATE PROFILE]", flat_number, email, alternate_phones, vehicle_numbers, home_locked, ownership_type)
    print("[DEBUG USER ID]", user_id)

    alt_phones_list = [p.strip() for p in alternate_phones.split(",") if p.strip()]
    # vehicle_list = [v.strip() for v in vehicle_numbers.split(",") if v.strip()]
    vehicle_list = vehicle_list = parse_vehicle_numbers(vehicle_numbers)

    update_data = {
        "flat_number": flat_number,
        "email": email,
        "alternate_phones": alt_phones_list,
        "vehicle_numbers": vehicle_list,
        "home_locked": home_locked,
        "ownership_type": ownership_type
    }

    response = supabase.table("users").update(update_data).eq("id", user_id.strip()).execute()
    print("[SUPABASE RESPONSE]", response)
    return RedirectResponse(url=f"/member/{user_id}", status_code=status.HTTP_302_FOUND)

@app.post("/add-payment")
def add_payment(user_id: str = Form(...), month_paid_for: str = Form(...), upi_reference: str = Form(...)):
    supabase.table("payments").insert({
        "user_id": user_id,
        "month_paid_for": month_paid_for,
        "upi_reference": upi_reference,
        "amount": 500
    }).execute()
    return RedirectResponse(url=f"/member/{user_id}", status_code=status.HTTP_302_FOUND)

# New route for admin dashboard template
@app.get("/admin-dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


