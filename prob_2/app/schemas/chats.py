from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ChatBase(BaseModel):
    user_id: UUID
    query: str

class ChatCreate(ChatBase):
    pass

class ChatInDBBase(ChatBase):
    id: UUID
    response: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
