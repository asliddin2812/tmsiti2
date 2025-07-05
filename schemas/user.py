from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Barcha foydalanuvchilarda mavjud bo‘lgan umumiy maydonlar
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_admin: bool = True
    is_active: bool = True

# Foydalanuvchi yaratishda parol ham kerak bo‘ladi
class UserCreate(UserBase):
    password: str

# Foydalanuvchini yangilashda har bir maydon ixtiyoriy bo‘ladi
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None

# Javobda qaytariladigan foydalanuvchi ma'lumotlari
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # ORM obyektini Pydantic modelga o‘tkazish uchun

# JWT token modeli (login javobida qaytadi)
class Token(BaseModel):
    access_token: str
    token_type: str

# JWT token ichidagi foydalanuvchi ma'lumoti
class TokenData(BaseModel):
    email: Optional[str] = None

# Login uchun kiruvchi ma’lumotlar
class UserLogin(BaseModel):
    email: EmailStr
    password: str
