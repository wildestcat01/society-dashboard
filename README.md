
# 🏠 Society Management Dashboard

A FastAPI + Supabase-based web app for managing housing society members, payments, expenses, and communication.

## ✨ Features

### 👤 Admin Dashboard
- Member Management (Add, Edit, Search)
- Monthly Payment Tracking (paid, unpaid, missed)
- Expense Recording & Reporting
- Defaulter Tracking
- Collection vs Expense & Unpaid Chart
- Notice Board Management

### 🧍 Member Dashboard
- QR Code UPI Payment
- Payment Status Grid
- Profile Update (Inline)
- Notice Display
- Member Directory (search)

## 🛠️ Tech Stack
- **Backend**: FastAPI, Supabase, Python
- **Frontend**: Jinja2 Templates, Tailwind CSS, Chart.js
- **Database**: PostgreSQL via Supabase

## 📦 Running Locally

```bash
git clone https://github.com/wildestcat01/society-dashboard.git
cd society-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Create `.env` file and add:
```
SUPABASE_URL=your-url
SUPABASE_KEY=your-service-role-key
```

## 🚀 Deployment

The app is deployed via [Render.com](https://render.com/).

---

## 📧 Contact
Made with ❤️ by Bilal. For collaboration or questions, raise an issue or email me.
