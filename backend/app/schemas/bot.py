from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class BotBase(BaseModel):
    """Базовая схема бота"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class BotCreate(BotBase):
    """Схема для создания бота"""
    token: str = Field(..., description="Telegram Bot Token")

class BotUpdate(BaseModel):
    """Схема для обновления бота"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    is_published: Optional[bool] = None
    settings: Optional[Dict[str, Any]] = None

class BotResponse(BotBase):
    """Схема ответа бота"""
    id: int
    user_id: int
    token: str
    is_active: bool
    is_published: bool
    users_count: int
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BotListResponse(BaseModel):
    """Схема списка ботов"""
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    is_published: bool
    users_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
