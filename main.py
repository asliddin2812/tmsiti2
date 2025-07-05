from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from core.config import settings
from core.database import Base, engine
from api import auth, institute, regulatory, activities, news, contact

# Create tables
Base.metadata.create_all(bind=engine)

# Create upload directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="TMSITI API",
    description="API for TMSITI Website",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(institute.router, prefix="/api/v1")
app.include_router(regulatory.router, prefix="/api/v1")
app.include_router(activities.router, prefix="/api/v1")
app.include_router(news.router, prefix="/api/v1")
app.include_router(contact.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "TMSITI API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return {"detail": "Not found"}

# Custom 500 handler
@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    return {"detail": "Internal server error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)