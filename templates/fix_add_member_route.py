
from fastapi import APIRouter, Form
from passlib.hash import bcrypt
from utils.supabase_client import supabase

router = APIRouter()

@router.post("/api/members")
def create_member(
    full_name: str = Form(...),
    mobile: str = Form(...),
    email: str = Form(None),
    flat_number: str = Form(None),
    vehicle_no: str = Form(None),
    ownership_type: str = Form(...),
    home_locked: str = Form(...),
    password: str = Form(...)
):
    encrypted_password = bcrypt.hash(password)

    response = supabase.table("users").insert({
        "full_name": full_name,
        "mobile": mobile,
        "email": email,
        "flat_number": flat_number,
        "vehicle_no": vehicle_no,
        "ownership_type": ownership_type,
        "home_locked": home_locked == "Yes",
        "password": encrypted_password,
        "role": "member"
    }).execute()

    return {"message": "Member added successfully", "data": response.data}
