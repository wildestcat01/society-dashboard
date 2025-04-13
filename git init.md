git init
git remote add origin https://github.com/wildestcat01/society-dashboard.git
git add .
git commit -m "Initial prod commit"
git push -u origin main


uvicorn main:app --reload 