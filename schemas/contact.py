from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ContactBase(BaseModel):
    location: str
    phone: str
    email: EmailStr
    exact_email: Optional[EmailStr] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    exact_email: Optional[EmailStr] = None

class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True