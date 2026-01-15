from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from datetime import datetime
from app.core.database import Base

class Connection(Base):
    """Связь между блоками"""
    __tablename__ = "connections"
    
    id = Column(Integer, primary_key=True, index=True)
    
    from_block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    to_block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    
    # Для условных переходов
    label = Column(String(50), nullable=True)  # "yes", "no", "buy", "skip", etc
    
    created_at = Column(DateTime, default=datetime.utcnow)
