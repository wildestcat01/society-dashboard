from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from utils.supabase_client import supabase

router = APIRouter()

@router.post("/update-notice")
def update_notice(request: Request, content: str = Form(...)):
    # Check if a notice already exists
    existing = supabase.table("notices").select("*").order("created_at", desc=True).limit(1).execute()

    if existing.data:
        notice_id = existing.data[0]["id"]
        # Update existing notice
        supabase.table("notices").update({"content": content}).eq("id", notice_id).execute()
    else:
        # Insert new if no notice exists
        supabase.table("notices").insert({"content": content}).execute()

    return RedirectResponse(url="/admin-dashboard", status_code=302)
