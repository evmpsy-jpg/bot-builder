from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConnectionBase(BaseModel):
    """Базовая схема связи"""
    from_block_id: int
    to_block_id: int
    label: Optional[str] = None

class ConnectionCreate(ConnectionBase):
    """Схема для создания связи"""
    pass

class ConnectionResponse(ConnectionBase):
    """Схема ответа связи"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
