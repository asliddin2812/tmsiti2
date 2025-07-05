from typing import List, Generic, TypeVar
from sqlalchemy.orm import Query
from schemas.common import PaginatedResponse
from math import ceil

T = TypeVar('T')

def paginate(query: Query, page: int = 1, size: int = 10) -> PaginatedResponse[T]:
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    if size > 100:
        size = 100
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    pages = ceil(total / size)
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )