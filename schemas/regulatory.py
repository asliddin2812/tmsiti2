from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ConstructionNormBase(BaseModel):
    subsystem: str
    group: str
    code: str
    title: str
    link: Optional[str] = None

class ConstructionNormCreate(ConstructionNormBase):
    pass

class ConstructionNormUpdate(BaseModel):
    subsystem: Optional[str] = None
    group: Optional[str] = None
    code: Optional[str] = None
    title: Optional[str] = None
    link: Optional[str] = None

class ConstructionNormResponse(ConstructionNormBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class StandardBase(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    link: Optional[str] = None

class StandardCreate(StandardBase):
    pass

class StandardUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None

class StandardResponse(StandardBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BuildingRegulationBase(BaseModel):
    number: str
    code: str
    title: str
    link: Optional[str] = None

class BuildingRegulationCreate(BuildingRegulationBase):
    pass

class BuildingRegulationUpdate(BaseModel):
    number: Optional[str] = None
    code: Optional[str] = None
    title: Optional[str] = None
    link: Optional[str] = None

class BuildingRegulationResponse(BuildingRegulationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CostResourceNormBase(BaseModel):
    srn_code: str
    srn_title: str
    main_shnq_code: str
    main_shnq_title: str
    additional_shnqs: Optional[List[Dict[str, Any]]] = None
    file: Optional[str] = None

class CostResourceNormCreate(CostResourceNormBase):
    pass

class CostResourceNormUpdate(BaseModel):
    srn_code: Optional[str] = None
    srn_title: Optional[str] = None
    main_shnq_code: Optional[str] = None
    main_shnq_title: Optional[str] = None
    additional_shnqs: Optional[List[Dict[str, Any]]] = None
    file: Optional[str] = None

class CostResourceNormResponse(CostResourceNormBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TechnicalRegulationBase(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    link: Optional[str] = None

class TechnicalRegulationCreate(TechnicalRegulationBase):
    pass

class TechnicalRegulationUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None

class TechnicalRegulationResponse(TechnicalRegulationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReferenceBase(BaseModel):
    number: str
    title: str
    link: Optional[str] = None

class ReferenceCreate(ReferenceBase):
    pass

class ReferenceUpdate(BaseModel):
    number: Optional[str] = None
    title: Optional[str] = None
    link: Optional[str] = None

class ReferenceResponse(ReferenceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True