from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.institute import About, Management, Structure, StructuralDivision, Vacancy
from schemas.institute import (
    AboutResponse, AboutCreate, AboutUpdate,
    ManagementResponse, ManagementCreate, ManagementUpdate,
    StructureResponse, StructureCreate, StructureUpdate,
    StructuralDivisionResponse, StructuralDivisionCreate, StructuralDivisionUpdate,
    VacancyResponse, VacancyCreate, VacancyUpdate
)
from schemas.common import PaginatedResponse, FileUploadResponse
from utils.dependencies import get_admin_user
from utils.pagination import paginate
from utils.file_handler import save_upload_file, delete_file

router = APIRouter(prefix="/institute", tags=["Institute"])

# About endpoints
@router.get("/about", response_model=List[AboutResponse])
async def get_about(db: Session = Depends(get_db)):
    return db.query(About).all()

@router.post("/about", response_model=AboutResponse)
async def create_about(
    about_data: AboutCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_about = About(**about_data.dict())
    db.add(db_about)
    db.commit()
    db.refresh(db_about)
    return db_about

@router.put("/about/{about_id}", response_model=AboutResponse)
async def update_about(
    about_id: int,
    about_data: AboutUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_about = db.query(About).filter(About.id == about_id).first()
    if not db_about:
        raise HTTPException(status_code=404, detail="About not found")
    
    update_data = about_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_about, field, value)
    
    db.commit()
    db.refresh(db_about)
    return db_about

@router.delete("/about/{about_id}")
async def delete_about(
    about_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_about = db.query(About).filter(About.id == about_id).first()
    if not db_about:
        raise HTTPException(status_code=404, detail="About not found")
    
    if db_about.pdf_url:
        delete_file(db_about.pdf_url)
    
    db.delete(db_about)
    db.commit()
    return {"message": "About deleted successfully"}

# Management endpoints
@router.get("/management", response_model=PaginatedResponse[ManagementResponse])
async def get_management(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Management).order_by(Management.order_index, Management.created_at)
    return paginate(query, page, size)

@router.post("/management", response_model=ManagementResponse)
async def create_management(
    management_data: ManagementCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_management = Management(**management_data.dict())
    db.add(db_management)
    db.commit()
    db.refresh(db_management)
    return db_management

@router.put("/management/{management_id}", response_model=ManagementResponse)
async def update_management(
    management_id: int,
    management_data: ManagementUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_management = db.query(Management).filter(Management.id == management_id).first()
    if not db_management:
        raise HTTPException(status_code=404, detail="Management not found")
    
    update_data = management_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_management, field, value)
    
    db.commit()
    db.refresh(db_management)
    return db_management

@router.delete("/management/{management_id}")
async def delete_management(
    management_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_management = db.query(Management).filter(Management.id == management_id).first()
    if not db_management:
        raise HTTPException(status_code=404, detail="Management not found")
    
    if db_management.profile_image:
        delete_file(db_management.profile_image)
    
    db.delete(db_management)
    db.commit()
    return {"message": "Management deleted successfully"}

# Structure endpoints
@router.get("/structure", response_model=List[StructureResponse])
async def get_structure(db: Session = Depends(get_db)):
    return db.query(Structure).all()

@router.post("/structure", response_model=StructureResponse)
async def create_structure(
    structure_data: StructureCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_structure = Structure(**structure_data.dict())
    db.add(db_structure)
    db.commit()
    db.refresh(db_structure)
    return db_structure

@router.put("/structure/{structure_id}", response_model=StructureResponse)
async def update_structure(
    structure_id: int,
    structure_data: StructureUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_structure = db.query(Structure).filter(Structure.id == structure_id).first()
    if not db_structure:
        raise HTTPException(status_code=404, detail="Structure not found")
    
    update_data = structure_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_structure, field, value)
    
    db.commit()
    db.refresh(db_structure)
    return db_structure

@router.delete("/structure/{structure_id}")
async def delete_structure(
    structure_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_structure = db.query(Structure).filter(Structure.id == structure_id).first()
    if not db_structure:
        raise HTTPException(status_code=404, detail="Structure not found")
    
    if db_structure.pdf_url:
        delete_file(db_structure.pdf_url)
    
    db.delete(db_structure)
    db.commit()
    return {"message": "Structure deleted successfully"}

# Structural Division endpoints
@router.get("/structural-divisions", response_model=PaginatedResponse[StructuralDivisionResponse])
async def get_structural_divisions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(StructuralDivision).order_by(StructuralDivision.created_at)
    return paginate(query, page, size)

@router.post("/structural-divisions", response_model=StructuralDivisionResponse)
async def create_structural_division(
    division_data: StructuralDivisionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_division = StructuralDivision(**division_data.dict())
    db.add(db_division)
    db.commit()
    db.refresh(db_division)
    return db_division

@router.put("/structural-divisions/{division_id}", response_model=StructuralDivisionResponse)
async def update_structural_division(
    division_id: int,
    division_data: StructuralDivisionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_division = db.query(StructuralDivision).filter(StructuralDivision.id == division_id).first()
    if not db_division:
        raise HTTPException(status_code=404, detail="Structural division not found")
    
    update_data = division_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_division, field, value)
    
    db.commit()
    db.refresh(db_division)
    return db_division

@router.delete("/structural-divisions/{division_id}")
async def delete_structural_division(
    division_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_division = db.query(StructuralDivision).filter(StructuralDivision.id == division_id).first()
    if not db_division:
        raise HTTPException(status_code=404, detail="Structural division not found")
    
    if db_division.profile_image:
        delete_file(db_division.profile_image)
    
    db.delete(db_division)
    db.commit()
    return {"message": "Structural division deleted successfully"}

# Vacancy endpoints
@router.get("/vacancies", response_model=PaginatedResponse[VacancyResponse])
async def get_vacancies(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    query = db.query(Vacancy)
    if active_only:
        query = query.filter(Vacancy.is_active == True)
    query = query.order_by(Vacancy.created_at.desc())
    return paginate(query, page, size)

@router.post("/vacancies", response_model=VacancyResponse)
async def create_vacancy(
    vacancy_data: VacancyCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_vacancy = Vacancy(**vacancy_data.dict())
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

@router.put("/vacancies/{vacancy_id}", response_model=VacancyResponse)
async def update_vacancy(
    vacancy_id: int,
    vacancy_data: VacancyUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    update_data = vacancy_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_vacancy, field, value)
    
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

@router.delete("/vacancies/{vacancy_id}")
async def delete_vacancy(
    vacancy_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    if db_vacancy.attachment:
        delete_file(db_vacancy.attachment)
    
    db.delete(db_vacancy)
    db.commit()
    return {"message": "Vacancy deleted successfully"}

# File upload endpoints
@router.post("/upload/image", response_model=FileUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    current_user = Depends(get_admin_user)
):
    file_path = await save_upload_file(file, "images")
    return FileUploadResponse(
        filename=file.filename,
        url=f"/uploads/{file_path}",
        size=file.size or 0
    )

@router.post("/upload/document", response_model=FileUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user = Depends(get_admin_user)
):
    file_path = await save_upload_file(file, "documents")
    return FileUploadResponse(
        filename=file.filename,
        url=f"/uploads/{file_path}",
        size=file.size or 0
    )