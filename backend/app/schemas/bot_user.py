from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class BotUserBase(BaseModel):
    """Базовая схема пользователя бота"""
    telegram_user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class BotUserResponse(BotUserBase):
    """Схема ответа пользователя бота"""
    id: int
    bot_id: int
    language_code: str
    is_blocked: bool
    current_flow_id: Optional[int]
    current_block_id: Optional[int]
    custom_fields: Dict[str, Any]
    last_message_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
