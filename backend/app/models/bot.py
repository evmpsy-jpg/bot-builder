from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from datetime import datetime
from app.core.database import Base

class Bot(Base):
    """Телеграм бот"""
    __tablename__ = "bots"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Основное
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    token = Column(String(200), unique=True, nullable=False)
    
    # Статус
    is_active = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    
    # Статистика
    users_count = Column(Integer, default=0)
    
    # Настройки
    settings = Column(JSON, default={})
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
