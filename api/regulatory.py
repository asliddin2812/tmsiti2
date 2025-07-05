from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.regulatory import (
    ConstructionNorm, Standard, BuildingRegulation, 
    CostResourceNorm, TechnicalRegulation, Reference
)
from schemas.regulatory import (
    ConstructionNormResponse, ConstructionNormCreate, ConstructionNormUpdate,
    StandardResponse, StandardCreate, StandardUpdate,
    BuildingRegulationResponse, BuildingRegulationCreate, BuildingRegulationUpdate,
    CostResourceNormResponse, CostResourceNormCreate, CostResourceNormUpdate,
    TechnicalRegulationResponse, TechnicalRegulationCreate, TechnicalRegulationUpdate,
    ReferenceResponse, ReferenceCreate, ReferenceUpdate
)
from schemas.common import PaginatedResponse, FileUploadResponse
from utils.dependencies import get_admin_user
from utils.pagination import paginate
from utils.file_handler import save_upload_file, delete_file

router = APIRouter(prefix="/regulatory", tags=["Regulatory Documents"])

# Construction Norms endpoints
@router.get("/construction-norms", response_model=PaginatedResponse[ConstructionNormResponse])
async def get_construction_norms(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    subsystem: Optional[str] = Query(None),
    group: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(ConstructionNorm)
    if subsystem:
        query = query.filter(ConstructionNorm.subsystem.ilike(f"%{subsystem}%"))
    if group:
        query = query.filter(ConstructionNorm.group.ilike(f"%{group}%"))
    query = query.order_by(ConstructionNorm.subsystem, ConstructionNorm.group, ConstructionNorm.code)
    return paginate(query, page, size)

@router.post("/construction-norms", response_model=ConstructionNormResponse)
async def create_construction_norm(
    norm_data: ConstructionNormCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_norm = ConstructionNorm(**norm_data.dict())
    db.add(db_norm)
    db.commit()
    db.refresh(db_norm)
    return db_norm

@router.put("/construction-norms/{norm_id}", response_model=ConstructionNormResponse)
async def update_construction_norm(
    norm_id: int,
    norm_data: ConstructionNormUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_norm = db.query(ConstructionNorm).filter(ConstructionNorm.id == norm_id).first()
    if not db_norm:
        raise HTTPException(status_code=404, detail="Construction norm not found")
    
    update_data = norm_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_norm, field, value)
    
    db.commit()
    db.refresh(db_norm)
    return db_norm

@router.delete("/construction-norms/{norm_id}")
async def delete_construction_norm(
    norm_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_norm = db.query(ConstructionNorm).filter(ConstructionNorm.id == norm_id).first()
    if not db_norm:
        raise HTTPException(status_code=404, detail="Construction norm not found")
    
    db.delete(db_norm)
    db.commit()
    return {"message": "Construction norm deleted successfully"}

# Standards endpoints
@router.get("/standards", response_model=PaginatedResponse[StandardResponse])
async def get_standards(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Standard)
    if search:
        query = query.filter(
            Standard.title.ilike(f"%{search}%") | 
            Standard.code.ilike(f"%{search}%")
        )
    query = query.order_by(Standard.code)
    return paginate(query, page, size)

@router.post("/standards", response_model=StandardResponse)
async def create_standard(
    standard_data: StandardCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_standard = Standard(**standard_data.dict())
    db.add(db_standard)
    db.commit()
    db.refresh(db_standard)
    return db_standard

@router.put("/standards/{standard_id}", response_model=StandardResponse)
async def update_standard(
    standard_id: int,
    standard_data: StandardUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_standard = db.query(Standard).filter(Standard.id == standard_id).first()
    if not db_standard:
        raise HTTPException(status_code=404, detail="Standard not found")
    
    update_data = standard_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_standard, field, value)
    
    db.commit()
    db.refresh(db_standard)
    return db_standard

@router.delete("/standards/{standard_id}")
async def delete_standard(
    standard_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_standard = db.query(Standard).filter(Standard.id == standard_id).first()
    if not db_standard:
        raise HTTPException(status_code=404, detail="Standard not found")
    
    db.delete(db_standard)
    db.commit()
    return {"message": "Standard deleted successfully"}

# Building Regulations endpoints
@router.get("/building-regulations", response_model=PaginatedResponse[BuildingRegulationResponse])
async def get_building_regulations(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(BuildingRegulation)
    if search:
        query = query.filter(
            BuildingRegulation.title.ilike(f"%{search}%") | 
            BuildingRegulation.code.ilike(f"%{search}%") |
            BuildingRegulation.number.ilike(f"%{search}%")
        )
    query = query.order_by(BuildingRegulation.number)
    return paginate(query, page, size)

@router.post("/building-regulations", response_model=BuildingRegulationResponse)
async def create_building_regulation(
    regulation_data: BuildingRegulationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_regulation = BuildingRegulation(**regulation_data.dict())
    db.add(db_regulation)
    db.commit()
    db.refresh(db_regulation)
    return db_regulation

@router.put("/building-regulations/{regulation_id}", response_model=BuildingRegulationResponse)
async def update_building_regulation(
    regulation_id: int,
    regulation_data: BuildingRegulationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_regulation = db.query(BuildingRegulation).filter(BuildingRegulation.id == regulation_id).first()
    if not db_regulation:
        raise HTTPException(status_code=404, detail="Building regulation not found")
    
    update_data = regulation_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_regulation, field, value)
    
    db.commit()
    db.refresh(db_regulation)
    return db_regulation

@router.delete("/building-regulations/{regulation_id}")
async def delete_building_regulation(
    regulation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_regulation = db.query(BuildingRegulation).filter(BuildingRegulation.id == regulation_id).first()
    if not db_regulation:
        raise HTTPException(status_code=404, detail="Building regulation not found")
    
    db.delete(db_regulation)
    db.commit()
    return {"message": "Building regulation deleted successfully"}

# Cost Resource Norms endpoints
@router.get("/cost-resource-norms", response_model=PaginatedResponse[CostResourceNormResponse])
async def get_cost_resource_norms(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(CostResourceNorm)
    if search:
        query = query.filter(
            CostResourceNorm.srn_title.ilike(f"%{search}%") |
            CostResourceNorm.srn_code.ilike(f"%{search}%")
        )
    query = query.order_by(CostResourceNorm.srn_code)
    return paginate(query, page, size)

@router.post("/cost-resource-norms", response_model=CostResourceNormResponse)
async def create_cost_resource_norm(
    norm_data: CostResourceNormCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_norm = CostResourceNorm(**norm_data.dict())
    db.add(db_norm)
    db.commit()
    db.refresh(db_norm)
    return db_norm

@router.put("/cost-resource-norms/{norm_id}", response_model=CostResourceNormResponse)
async def update_cost_resource_norm(
    norm_id: int,
    norm_data: CostResourceNormUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_norm = db.query(CostResourceNorm).filter(CostResourceNorm.id == norm_id).first()
    if not db_norm:
        raise HTTPException(status_code=404, detail="Cost resource norm not found")
    
    update_data = norm_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_norm, field, value)
    
    db.commit()
    db.refresh(db_norm)
    return db_norm

@router.delete("/cost-resource-norms/{norm_id}")
async def delete_cost_resource_norm(
    norm_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_norm = db.query(CostResourceNorm).filter(CostResourceNorm.id == norm_id).first()
    if not db_norm:
        raise HTTPException(status_code=404, detail="Cost resource norm not found")
    
    if db_norm.file:
        delete_file(db_norm.file)
    
    db.delete(db_norm)
    db.commit()
    return {"message": "Cost resource norm deleted successfully"}

# Technical Regulations endpoints
@router.get("/technical-regulations", response_model=PaginatedResponse[TechnicalRegulationResponse])
async def get_technical_regulations(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(TechnicalRegulation)
    if search:
        query = query.filter(
            TechnicalRegulation.title.ilike(f"%{search}%") |
            TechnicalRegulation.code.ilike(f"%{search}%")
        )
    query = query.order_by(TechnicalRegulation.code)
    return paginate(query, page, size)

@router.post("/technical-regulations", response_model=TechnicalRegulationResponse)
async def create_technical_regulation(
    regulation_data: TechnicalRegulationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_regulation = TechnicalRegulation(**regulation_data.dict())
    db.add(db_regulation)
    db.commit()
    db.refresh(db_regulation)
    return db_regulation

@router.put("/technical-regulations/{regulation_id}", response_model=TechnicalRegulationResponse)
async def update_technical_regulation(
    regulation_id: int,
    regulation_data: TechnicalRegulationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_regulation = db.query(TechnicalRegulation).filter(TechnicalRegulation.id == regulation_id).first()
    if not db_regulation:
        raise HTTPException(status_code=404, detail="Technical regulation not found")
    
    update_data = regulation_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_regulation, field, value)
    
    db.commit()
    db.refresh(db_regulation)
    return db_regulation

@router.delete("/technical-regulations/{regulation_id}")
async def delete_technical_regulation(
    regulation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_regulation = db.query(TechnicalRegulation).filter(TechnicalRegulation.id == regulation_id).first()
    if not db_regulation:
        raise HTTPException(status_code=404, detail="Technical regulation not found")
    
    db.delete(db_regulation)
    db.commit()
    return {"message": "Technical regulation deleted successfully"}

# References endpoints
@router.get("/references", response_model=PaginatedResponse[ReferenceResponse])
async def get_references(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Reference)
    if search:
        query = query.filter(
            Reference.title.ilike(f"%{search}%") |
            Reference.number.ilike(f"%{search}%")
        )
    query = query.order_by(Reference.number)
    return paginate(query, page, size)

@router.post("/references", response_model=ReferenceResponse)
async def create_reference(
    reference_data: ReferenceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_reference = Reference(**reference_data.dict())
    db.add(db_reference)
    db.commit()
    db.refresh(db_reference)
    return db_reference

@router.put("/references/{reference_id}", response_model=ReferenceResponse)
async def update_reference(
    reference_id: int,
    reference_data: ReferenceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_reference = db.query(Reference).filter(Reference.id == reference_id).first()
    if not db_reference:
        raise HTTPException(status_code=404, detail="Reference not found")
    
    update_data = reference_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reference, field, value)
    
    db.commit()
    db.refresh(db_reference)
    return db_reference

@router.delete("/references/{reference_id}")
async def delete_reference(
    reference_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_reference = db.query(Reference).filter(Reference.id == reference_id).first()
    if not db_reference:
        raise HTTPException(status_code=404, detail="Reference not found")
    
    db.delete(db_reference)
    db.commit()
    return {"message": "Reference deleted successfully"}

# File upload for regulatory documents
@router.post("/upload/document", response_model=FileUploadResponse)
async def upload_regulatory_document(
    file: UploadFile = File(...),
    current_user = Depends(get_admin_user)
):
    file_path = await save_upload_file(file, "regulatory")
    return FileUploadResponse(
        filename=file.filename,
        url=f"/uploads/{file_path}",
        size=file.size or 0
    )