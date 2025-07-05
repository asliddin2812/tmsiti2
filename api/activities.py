from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.activities import ManagementSystem
from schemas.activities import (
    ManagementSystemResponse, ManagementSystemCreate, ManagementSystemUpdate
)
from schemas.common import PaginatedResponse, FileUploadResponse
from utils.dependencies import get_admin_user
from utils.pagination import paginate
from utils.file_handler import save_upload_file, delete_file

router = APIRouter(prefix="/activities", tags=["Activities"])

# Management Systems endpoints
@router.get("/management-systems", response_model=PaginatedResponse[ManagementSystemResponse])
async def get_management_systems(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(ManagementSystem)
    if search:
        query = query.filter(ManagementSystem.title.ilike(f"%{search}%"))
    query = query.order_by(ManagementSystem.created_at.desc())
    return paginate(query, page, size)

@router.post("/management-systems", response_model=ManagementSystemResponse)
async def create_management_system(
    system_data: ManagementSystemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_system = ManagementSystem(**system_data.dict())
    db.add(db_system)
    db.commit()
    db.refresh(db_system)
    return db_system

@router.put("/management-systems/{system_id}", response_model=ManagementSystemResponse)
async def update_management_system(
    system_id: int,
    system_data: ManagementSystemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_system = db.query(ManagementSystem).filter(ManagementSystem.id == system_id).first()
    if not db_system:
        raise HTTPException(status_code=404, detail="Management system not found")
    
    update_data = system_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_system, field, value)
    
    db.commit()
    db.refresh(db_system)
    return db_system

@router.delete("/management-systems/{system_id}")
async def delete_management_system(
    system_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_system = db.query(ManagementSystem).filter(ManagementSystem.id == system_id).first()
    if not db_system:
        raise HTTPException(status_code=404, detail="Management system not found")
    
    if db_system.pdf:
        delete_file(db_system.pdf)
    
    db.delete(db_system)
    db.commit()
    return {"message": "Management system deleted successfully"}

# File upload for activities
@router.post("/upload/document", response_model=FileUploadResponse)
async def upload_activity_document(
    file: UploadFile = File(...),
    current_user = Depends(get_admin_user)
):
    file_path = await save_upload_file(file, "activities")
    return FileUploadResponse(
        filename=file.filename,
        url=f"/uploads/{file_path}",
        size=file.size or 0
    )