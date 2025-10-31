# app/main.py
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from app.database import prisma, connect_db, disconnect_db

# Health route
async def health(request):
    return JSONResponse({"status": "ok"})

# Test DB connectivity
async def db_check(request):
    try:
        result = await prisma.execute_raw("SELECT 1;")
        return JSONResponse({"db_status": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# Define routes
routes = [
    Route("/", endpoint=health, methods=["GET"]),
    Route("/db-check", endpoint=db_check, methods=["GET"]),
]

# Create Starlette app
app = Starlette(debug=True, routes=routes)

# Connect/disconnect DB during app lifecycle
@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
