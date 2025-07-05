from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AboutBase(BaseModel):
    content: str
    pdf_url: Optional[str] = None

class AboutCreate(AboutBase):
    pass

class AboutUpdate(BaseModel):
    content: Optional[str] = None
    pdf_url: Optional[str] = None

class AboutResponse(AboutBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ManagementBase(BaseModel):
    full_name: str
    position: str
    profile_image: Optional[str] = None
    reception_days: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    specialization: Optional[str] = None
    order_index: int = 0

class ManagementCreate(ManagementBase):
    pass

class ManagementUpdate(BaseModel):
    full_name: Optional[str] = None
    position: Optional[str] = None
    profile_image: Optional[str] = None
    reception_days: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    specialization: Optional[str] = None
    order_index: Optional[int] = None

class ManagementResponse(ManagementBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class StructureBase(BaseModel):
    title: str
    pdf_url: str

class StructureCreate(StructureBase):
    pass

class StructureUpdate(BaseModel):
    title: Optional[str] = None
    pdf_url: Optional[str] = None

class StructureResponse(StructureBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class StructuralDivisionBase(BaseModel):
    title: str
    head_full_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_image: Optional[str] = None

class StructuralDivisionCreate(StructuralDivisionBase):
    pass

class StructuralDivisionUpdate(BaseModel):
    title: Optional[str] = None
    head_full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_image: Optional[str] = None

class StructuralDivisionResponse(StructuralDivisionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class VacancyBase(BaseModel):
    title: str
    description: str
    requirements: str
    deadline: Optional[datetime] = None
    contact_email: EmailStr
    attachment: Optional[str] = None
    is_active: bool = True

class VacancyCreate(VacancyBase):
    pass

class VacancyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    deadline: Optional[datetime] = None
    contact_email: Optional[EmailStr] = None
    attachment: Optional[str] = None
    is_active: Optional[bool] = None

class VacancyResponse(VacancyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True