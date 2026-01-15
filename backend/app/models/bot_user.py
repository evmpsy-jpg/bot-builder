from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from datetime import datetime
from app.core.database import Base

class BotUser(Base):
    """Пользователь бота в Telegram"""
    __tablename__ = "bot_users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False, index=True)
    telegram_user_id = Column(Integer, nullable=False, index=True)
    
    # Telegram данные
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    language_code = Column(String(10), default="en")
    
    # Состояние
    is_blocked = Column(Boolean, default=False)
    current_flow_id = Column(Integer, ForeignKey("flows.id"), nullable=True)
    current_block_id = Column(Integer, nullable=True)
    
    # Кастомные поля (для форм)
    custom_fields = Column(JSON, default={})
    
    # Метаданные
    last_message_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
