from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from datetime import datetime
from app.core.database import Base

class Flow(Base):
    """Flow (сценарий/автоматизация бота)"""
    __tablename__ = "flows"
    
    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False, index=True)
    
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Статус
    is_active = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    
    # Начальный блок
    start_block_id = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
