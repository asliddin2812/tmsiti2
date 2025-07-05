import os
import shutil
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from core.config import settings

ALLOWED_EXTENSIONS = {
    'image': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'},
    'document': {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'},
    'archive': {'.zip', '.rar', '.7z', '.tar', '.gz'}
}

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def is_allowed_file(filename: str, file_type: str = None) -> bool:
    ext = get_file_extension(filename)
    if file_type and file_type in ALLOWED_EXTENSIONS:
        return ext in ALLOWED_EXTENSIONS[file_type]
    
    all_extensions = set()
    for extensions in ALLOWED_EXTENSIONS.values():
        all_extensions.update(extensions)
    return ext in all_extensions

def generate_unique_filename(filename: str) -> str:
    ext = get_file_extension(filename)
    unique_name = str(uuid.uuid4())
    return f"{unique_name}{ext}"

async def save_upload_file(file: UploadFile, folder: str = "general") -> str:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Check file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(settings.UPLOAD_DIR, folder)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    unique_filename = generate_unique_filename(file.filename)
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    return f"{folder}/{unique_filename}"

def delete_file(file_path: str) -> bool:
    try:
        full_path = os.path.join(settings.UPLOAD_DIR, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    except Exception:
        return False