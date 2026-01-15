from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FlowBase(BaseModel):
    """Базовая схема flow"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class FlowCreate(FlowBase):
    """Схема для создания flow"""
    bot_id: int

class FlowUpdate(BaseModel):
    """Схема для обновления flow"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    is_published: Optional[bool] = None
    start_block_id: Optional[int] = None

class FlowResponse(FlowBase):
    """Схема ответа flow"""
    id: int
    bot_id: int
    is_active: bool
    is_published: bool
    start_block_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class FlowListResponse(BaseModel):
    """Схема списка flows"""
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    is_published: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
