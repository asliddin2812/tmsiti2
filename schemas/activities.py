from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ManagementSystemBase(BaseModel):
    title: str
    description: str
    pdf: Optional[str] = None

class ManagementSystemCreate(ManagementSystemBase):
    pass

class ManagementSystemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    pdf: Optional[str] = None

class ManagementSystemResponse(ManagementSystemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True