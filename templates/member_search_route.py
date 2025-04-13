
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.supabase_client import supabase

router = APIRouter()

@router.get("/search-members")
def search_members(query: str = ""):
    try:
        if query:
            filters = (
                f"and(role.eq.member,full_name.ilike.*{query}*),"
                f"and(role.eq.member,mobile.ilike.*{query}*),"
                f"and(role.eq.member,flat_number.ilike.*{query}*),"
                f"and(role.eq.member,vehicle_no.ilike.*{query}*)"
            )
            r = supabase.table("users").select("*").or_(filters).execute()
        else:
            r = supabase.table("users").select("*").eq("role", "member").execute()

        return JSONResponse({"results": r.data})
    except Exception as e:
        print("[ERROR] Search failed:", e)
        return JSONResponse({"results": [], "error": str(e)})
