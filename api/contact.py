from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.contact import Contact
from schemas.contact import ContactResponse, ContactCreate, ContactUpdate
from utils.dependencies import get_admin_user

router = APIRouter(prefix="/contact", tags=["Contact"])

@router.get("/", response_model=List[ContactResponse])
async def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()

@router.post("/", response_model=ContactResponse)
async def create_contact(
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_contact = Contact(**contact_data.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    update_data = contact_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_contact, field, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted successfully"}