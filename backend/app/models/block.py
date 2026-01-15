from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from datetime import datetime
from app.core.database import Base

class Block(Base):
    """Блок в Flow"""
    __tablename__ = "blocks"
    
    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(Integer, ForeignKey("flows.id"), nullable=False, index=True)
    
    title = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # TEXT_MESSAGE, BUTTONS, CONDITION, etc
    
    # Контент блока (зависит от типа)
    content = Column(JSON, nullable=False, default={})
    
    # Позиция на канвасе (для визуального редактора)
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
