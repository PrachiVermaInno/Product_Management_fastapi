from fastapi import FastAPI
from app.routers import file_router
from app.database import engine, Base

app = FastAPI(title="Product File Handling API")

Base.metadata.create_all(bind=engine)
app.include_router(file_router.router)
