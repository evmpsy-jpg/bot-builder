from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class BlockBase(BaseModel):
    """Базовая схема блока"""
    title: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., description="TEXT_MESSAGE, BUTTONS, CONDITION, etc")
    content: Dict[str, Any] = Field(default_factory=dict)

class BlockCreate(BlockBase):
    """Схема для создания блока"""
    flow_id: int
    position_x: int = 0
    position_y: int = 0

class BlockUpdate(BaseModel):
    """Схема для обновления блока"""
    title: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    position_x: Optional[int] = None
    position_y: Optional[int] = None

class BlockResponse(BlockBase):
    """Схема ответа блока"""
    id: int
    flow_id: int
    position_x: int
    position_y: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
