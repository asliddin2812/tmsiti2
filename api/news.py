from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.news import Announcement, News, Meeting, AntiCorruption
from schemas.news import (
    AnnouncementResponse, AnnouncementCreate, AnnouncementUpdate,
    NewsResponse, NewsCreate, NewsUpdate,
    MeetingResponse, MeetingCreate, MeetingUpdate,
    AntiCorruptionResponse, AntiCorruptionCreate, AntiCorruptionUpdate
)
from schemas.common import PaginatedResponse, FileUploadResponse
from utils.dependencies import get_admin_user
from utils.pagination import paginate
from utils.file_handler import save_upload_file, delete_file

router = APIRouter(prefix="/news", tags=["News & Information"])

# Announcements endpoints
@router.get("/announcements", response_model=PaginatedResponse[AnnouncementResponse])
async def get_announcements(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    query = db.query(Announcement)
    if active_only:
        query = query.filter(Announcement.is_active == True)
    query = query.order_by(Announcement.created_at.desc())
    return paginate(query, page, size)

@router.post("/announcements", response_model=AnnouncementResponse)
async def create_announcement(
    announcement_data: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_announcement = Announcement(**announcement_data.dict())
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

@router.put("/announcements/{announcement_id}", response_model=AnnouncementResponse)
async def update_announcement(
    announcement_id: int,
    announcement_data: AnnouncementUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    update_data = announcement_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_announcement, field, value)
    
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

@router.delete("/announcements/{announcement_id}")
async def delete_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    if db_announcement.attachment:
        delete_file(db_announcement.attachment)
    
    db.delete(db_announcement)
    db.commit()
    return {"message": "Announcement deleted successfully"}

# News endpoints
@router.get("/news", response_model=PaginatedResponse[NewsResponse])
async def get_news(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    published_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    query = db.query(News)
    if published_only:
        query = query.filter(News.is_published == True)
    query = query.order_by(News.created_at.desc())
    return paginate(query, page, size)

@router.post("/news", response_model=NewsResponse)
async def create_news(
    news_data: NewsCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_news = News(**news_data.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

@router.put("/news/{news_id}", response_model=NewsResponse)
async def update_news(
    news_id: int,
    news_data: NewsUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_news = db.query(News).filter(News.id == news_id).first()
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    
    update_data = news_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_news, field, value)
    
    db.commit()
    db.refresh(db_news)
    return db_news

@router.delete("/news/{news_id}")
async def delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_news = db.query(News).filter(News.id == news_id).first()
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    
    if db_news.image:
        delete_file(db_news.image)
    
    db.delete(db_news)
    db.commit()
    return {"message": "News deleted successfully"}

# Meetings endpoints
@router.get("/meetings", response_model=PaginatedResponse[MeetingResponse])
async def get_meetings(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Meeting).order_by(Meeting.meeting_date.desc().nullslast(), Meeting.created_at.desc())
    return paginate(query, page, size)

@router.post("/meetings", response_model=MeetingResponse)
async def create_meeting(
    meeting_data: MeetingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_meeting = Meeting(**meeting_data.dict())
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

@router.put("/meetings/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(
    meeting_id: int,
    meeting_data: MeetingUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    update_data = meeting_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_meeting, field, value)
    
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

@router.delete("/meetings/{meeting_id}")
async def delete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    if db_meeting.attachment:
        delete_file(db_meeting.attachment)
    
    db.delete(db_meeting)
    db.commit()
    return {"message": "Meeting deleted successfully"}

# Anti-corruption endpoints
@router.get("/anti-corruption", response_model=PaginatedResponse[AntiCorruptionResponse])
async def get_anti_corruption(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(AntiCorruption).order_by(AntiCorruption.created_at.desc())
    return paginate(query, page, size)

@router.post("/anti-corruption", response_model=AntiCorruptionResponse)
async def create_anti_corruption(
    anti_corruption_data: AntiCorruptionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_anti_corruption = AntiCorruption(**anti_corruption_data.dict())
    db.add(db_anti_corruption)
    db.commit()
    db.refresh(db_anti_corruption)
    return db_anti_corruption

@router.put("/anti-corruption/{anti_corruption_id}", response_model=AntiCorruptionResponse)
async def update_anti_corruption(
    anti_corruption_id: int,
    anti_corruption_data: AntiCorruptionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_anti_corruption = db.query(AntiCorruption).filter(AntiCorruption.id == anti_corruption_id).first()
    if not db_anti_corruption:
        raise HTTPException(status_code=404, detail="Anti-corruption item not found")
    
    update_data = anti_corruption_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_anti_corruption, field, value)
    
    db.commit()
    db.refresh(db_anti_corruption)
    return db_anti_corruption

@router.delete("/anti-corruption/{anti_corruption_id}")
async def delete_anti_corruption(
    anti_corruption_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_anti_corruption = db.query(AntiCorruption).filter(AntiCorruption.id == anti_corruption_id).first()
    if not db_anti_corruption:
        raise HTTPException(status_code=404, detail="Anti-corruption item not found")
    
    if db_anti_corruption.document:
        delete_file(db_anti_corruption.document)
    
    db.delete(db_anti_corruption)
    db.commit()
    return {"message": "Anti-corruption item deleted successfully"}

# File upload for news
@router.post("/upload/image", response_model=FileUploadResponse)
async def upload_news_image(
    file: UploadFile = File(...),
    current_user = Depends(get_admin_user)
):
    file_path = await save_upload_file(file, "news/images")
    return FileUploadResponse(
        filename=file.filename,
        url=f"/uploads/{file_path}",
        size=file.size or 0
    )

@router.post("/upload/document", response_model=FileUploadResponse)
async def upload_news_document(
    file: UploadFile = File(...),
    current_user = Depends(get_admin_user)
):
    file_path = await save_upload_file(file, "news/documents")
    return FileUploadResponse(
        filename=file.filename,
        url=f"/uploads/{file_path}",
        size=file.size or 0
    )