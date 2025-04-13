import os
from dotenv import load_dotenv
from supabase import create_client, Client
from passlib.hash import bcrypt

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_user():
    full_name = input("Full Name: ")
    mobile = input("Mobile Number: ")
    password = input("Password: ")
    flat_number = input("Flat Number: ")
    vehicle_no = input("Vehicle Number: ")
    role = input("Role (admin/member): ").strip().lower()

    hashed_password = bcrypt.hash(password)

    response = supabase.table("users").insert({
        "full_name": full_name,
        "mobile": mobile,
        "password": hashed_password,
        "flat_number": flat_number,
        "vehicle_no": vehicle_no,
        "role": role
    }).execute()

    print("✅ User created:", response)

if __name__ == "__main__":
    create_user()
