
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from utils.supabase_client import supabase
from passlib.hash import bcrypt
import json

router = APIRouter()

@router.post("/add-member")
def add_member(
    request: Request,
    full_name: str = Form(...),
    mobile: str = Form(...),
    email: str = Form(""),
    flat_number: str = Form(...),
    password: str = Form(...),
    alternate_phones: str = Form(""),
    vehicle_numbers: str = Form(""),
    ownership_type: str = Form("Owned"),
    home_locked: bool = Form(False),
    is_active: bool = Form(True)
):
    hashed_password = bcrypt.hash(password)

    data = {
        "full_name": full_name,
        "mobile": mobile,
        "email": email,
        "flat_number": flat_number,
        "password": hashed_password,
        "alternate_phones": json.loads(alternate_phones) if alternate_phones else [],
        "vehicle_numbers": json.loads(vehicle_numbers) if vehicle_numbers else [],
        "ownership_type": ownership_type,
        "home_locked": home_locked,
        "is_active": is_active,
        "role": "member"
    }

    supabase.table("users").insert(data).execute()
    return RedirectResponse(url="/admin-dashboard", status_code=302)

@router.post("/edit-member/{member_id}")
def edit_member(
    member_id: str,
    request: Request,
    full_name: str = Form(...),
    mobile: str = Form(...),
    email: str = Form(""),
    flat_number: str = Form(...),
    alternate_phones: str = Form(""),
    vehicle_numbers: str = Form(""),
    ownership_type: str = Form("Owned"),
    home_locked: bool = Form(False),
    is_active: bool = Form(True)
):
    data = {
        "full_name": full_name,
        "mobile": mobile,
        "email": email,
        "flat_number": flat_number,
        "alternate_phones": json.loads(alternate_phones) if alternate_phones else [],
        "vehicle_numbers": json.loads(vehicle_numbers) if vehicle_numbers else [],
        "ownership_type": ownership_type,
        "home_locked": home_locked,
        "is_active": is_active,
    }

    supabase.table("users").update(data).eq("id", member_id).execute()
    return RedirectResponse(url="/admin-dashboard", status_code=302)
