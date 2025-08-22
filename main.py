from fastapi import FastAPI
from routers import process, uploads, health

app = FastAPI(title="Uploader API", version="1.0.0")

app.include_router(uploads.router, prefix="/api", tags=["uploads"])
app.include_router(process.router, prefix="/api", tags=["process"])
app.include_router(health.router, tags=["health"])
