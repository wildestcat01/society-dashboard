
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from utils.supabase_client import supabase
import bcrypt
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse




router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/logout")
def logout(request: Request):
    request.session.clear()  # Clear session
    return RedirectResponse("/", status_code=302)


@router.get("/")
def root_redirect():
    return RedirectResponse(url="/login", status_code=302)

@router.get("/login")
def show_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_user(
    request: Request,
    mobile: str = Form(...),
    password: str = Form(...)
):
    response = supabase.table("users").select("*").eq("mobile", mobile).execute()

    if response.data:
        user = response.data[0]
        stored_hash = user["password"].encode("utf-8")
        typed_password = password.encode("utf-8")

        if bcrypt.checkpw(typed_password, stored_hash):
            request.session["user_id"] = user["id"]
            request.session["role"] = user["role"]

            if user["role"] == "admin":
                return RedirectResponse(url="/admin-dashboard", status_code=302)
            else:
                return RedirectResponse(url=f"/member/{user['id']}", status_code=302)

    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Invalid mobile number or password"
    })



@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)
