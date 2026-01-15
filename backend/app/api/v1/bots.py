from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.bot import Bot
from app.schemas.bot import (
    BotCreate,
    BotUpdate,
    BotResponse,
    BotListResponse
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bots", tags=["bots"])

@router.post("", response_model=BotResponse, status_code=status.HTTP_201_CREATED)
async def create_bot(
    bot_data: BotCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать нового бота"""
    
    user_id = int(current_user["sub"])
    
    # Проверяем уникальность токена
    existing_bot = db.query(Bot).filter(Bot.token == bot_data.token).first()
    if existing_bot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bot with this token already exists"
        )
    
    # Создаем бота
    bot = Bot(
        user_id=user_id,
        name=bot_data.name,
        description=bot_data.description,
        token=bot_data.token
    )
    
    db.add(bot)
    db.commit()
    db.refresh(bot)
    
    logger.info(f"Bot created: {bot.name} (ID: {bot.id}) by user {user_id}")
    
    return BotResponse.from_orm(bot)

@router.get("", response_model=List[BotListResponse])
async def get_bots(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Получить список ботов текущего пользователя"""
    
    user_id = int(current_user["sub"])
    
    bots = db.query(Bot).filter(
        Bot.user_id == user_id
    ).offset(skip).limit(limit).all()
    
    return [BotListResponse.from_orm(bot) for bot in bots]

@router.get("/{bot_id}", response_model=BotResponse)
async def get_bot(
    bot_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить бота по ID"""
    
    user_id = int(current_user["sub"])
    
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    
    return BotResponse.from_orm(bot)

@router.put("/{bot_id}", response_model=BotResponse)
async def update_bot(
    bot_id: int,
    bot_data: BotUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить бота"""
    
    user_id = int(current_user["sub"])
    
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    
    # Обновляем поля
    update_data = bot_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bot, field, value)
    
    db.commit()
    db.refresh(bot)
    
    logger.info(f"Bot updated: {bot.name} (ID: {bot.id})")
    
    return BotResponse.from_orm(bot)

@router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot(
    bot_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить бота"""
    
    user_id = int(current_user["sub"])
    
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    
    db.delete(bot)
    db.commit()
    
    logger.info(f"Bot deleted: {bot.name} (ID: {bot.id})")
    
    return None
