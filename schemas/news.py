from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnnouncementBase(BaseModel):
    title: str
    content: str
    attachment: Optional[str] = None
    is_active: bool = True

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    attachment: Optional[str] = None
    is_active: Optional[bool] = None

class AnnouncementResponse(AnnouncementBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class NewsBase(BaseModel):
    title: str
    content: str
    image: Optional[str] = None
    is_published: bool = True

class NewsCreate(NewsBase):
    pass

class NewsUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    is_published: Optional[bool] = None

class NewsResponse(NewsBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MeetingBase(BaseModel):
    title: str
    content: str
    meeting_date: Optional[datetime] = None
    location: Optional[str] = None
    attachment: Optional[str] = None

class MeetingCreate(MeetingBase):
    pass

class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    meeting_date: Optional[datetime] = None
    location: Optional[str] = None
    attachment: Optional[str] = None

class MeetingResponse(MeetingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AntiCorruptionBase(BaseModel):
    title: str
    content: str
    document: Optional[str] = None

class AntiCorruptionCreate(AntiCorruptionBase):
    pass

class AntiCorruptionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    document: Optional[str] = None

class AntiCorruptionResponse(AntiCorruptionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True