
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from utils.supabase_client import supabase
from datetime import datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta
import csv
import io

router = APIRouter()

@router.get("/export-defaulters")
def export_defaulters_csv():
    now = datetime.now()

    members = supabase.table("users").select("*").eq("role", "member").execute().data or []
    payments = supabase.table("payments").select("*").execute().data or []

    # Map payments per member by month
    paid_map = defaultdict(set)
    for p in payments:
        paid_map[p["user_id"]].add(p["month_paid_for"][:7])

    # Compile defaulter data
    defaulters = []
    for m in members:
        enrollment = m.get("enrollment_date")
        if not enrollment:
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
            defaulters.append({
                "name": m.get("full_name", ""),
                "flat": m.get("flat_number", ""),
                "mobile": m.get("mobile", ""),
                "unpaid_months": ", ".join(unpaid_months)
            })

    # Stream CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["name", "flat", "mobile", "unpaid_months"])
    writer.writeheader()
    for row in defaulters:
        writer.writerow(row)
    output.seek(0)

    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=defaulters.csv"
    })
