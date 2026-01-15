from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.bot import Bot
from app.models.flow import Flow
from app.models.block import Block
from app.models.connection import Connection
from app.schemas.flow import (
    FlowCreate,
    FlowUpdate,
    FlowResponse,
    FlowListResponse
)
from app.schemas.block import BlockCreate, BlockUpdate, BlockResponse
from app.schemas.connection import ConnectionCreate, ConnectionResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/flows", tags=["flows"])

# ============ FLOWS ============

@router.post("", response_model=FlowResponse, status_code=status.HTTP_201_CREATED)
async def create_flow(
    flow_data: FlowCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новый flow"""
    
    user_id = int(current_user["sub"])
    
    # Проверяем что бот принадлежит пользователю
    bot = db.query(Bot).filter(
        Bot.id == flow_data.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    
    # Создаем flow
    flow = Flow(
        bot_id=flow_data.bot_id,
        name=flow_data.name,
        description=flow_data.description
    )
    
    db.add(flow)
    db.commit()
    db.refresh(flow)
    
    logger.info(f"Flow created: {flow.name} (ID: {flow.id}) for bot {bot.id}")
    
    return FlowResponse.from_orm(flow)

@router.get("", response_model=List[FlowListResponse])
async def get_flows(
    bot_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Получить список flows для бота"""
    
    user_id = int(current_user["sub"])
    
    # Проверяем что бот принадлежит пользователю
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    
    flows = db.query(Flow).filter(
        Flow.bot_id == bot_id
    ).offset(skip).limit(limit).all()
    
    return [FlowListResponse.from_orm(flow) for flow in flows]

@router.get("/{flow_id}", response_model=FlowResponse)
async def get_flow(
    flow_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить flow по ID"""
    
    user_id = int(current_user["sub"])
    
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    # Проверяем что бот принадлежит пользователю
    bot = db.query(Bot).filter(
        Bot.id == flow.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return FlowResponse.from_orm(flow)

@router.put("/{flow_id}", response_model=FlowResponse)
async def update_flow(
    flow_id: int,
    flow_data: FlowUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить flow"""
    
    user_id = int(current_user["sub"])
    
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    # Проверяем что бот принадлежит пользователю
    bot = db.query(Bot).filter(
        Bot.id == flow.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Обновляем поля
    update_data = flow_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(flow, field, value)
    
    db.commit()
    db.refresh(flow)
    
    logger.info(f"Flow updated: {flow.name} (ID: {flow.id})")
    
    return FlowResponse.from_orm(flow)

@router.delete("/{flow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flow(
    flow_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить flow"""
    
    user_id = int(current_user["sub"])
    
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    # Проверяем что бот принадлежит пользователю
    bot = db.query(Bot).filter(
        Bot.id == flow.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(flow)
    db.commit()
    
    logger.info(f"Flow deleted: {flow.name} (ID: {flow.id})")
    
    return None

# ============ BLOCKS ============

@router.post("/{flow_id}/blocks", response_model=BlockResponse, status_code=status.HTTP_201_CREATED)
async def create_block(
    flow_id: int,
    block_data: BlockCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать блок в flow"""
    
    user_id = int(current_user["sub"])
    
    # Проверяем доступ к flow
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    bot = db.query(Bot).filter(
        Bot.id == flow.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Создаем блок
    block = Block(
        flow_id=flow_id,
        title=block_data.title,
        type=block_data.type,
        content=block_data.content,
        position_x=block_data.position_x,
        position_y=block_data.position_y
    )
    
    db.add(block)
    db.commit()
    db.refresh(block)
    
    logger.info(f"Block created: {block.title} (ID: {block.id}) in flow {flow_id}")
    
    return BlockResponse.from_orm(block)

@router.get("/{flow_id}/blocks", response_model=List[BlockResponse])
async def get_blocks(
    flow_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить все блоки flow"""
    
    user_id = int(current_user["sub"])
    
    # Проверяем доступ
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    bot = db.query(Bot).filter(
        Bot.id == flow.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    blocks = db.query(Block).filter(Block.flow_id == flow_id).all()
    
    return [BlockResponse.from_orm(block) for block in blocks]

@router.put("/{flow_id}/blocks/{block_id}", response_model=BlockResponse)
async def update_block(
    flow_id: int,
    block_id: int,
    block_data: BlockUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить блок"""
    
    user_id = int(current_user["sub"])
    
    block = db.query(Block).filter(
        Block.id == block_id,
        Block.flow_id == flow_id
    ).first()
    
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Block not found"
        )
    
    # Проверяем доступ
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    bot = db.query(Bot).filter(
        Bot.id == flow.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Обновляем поля
    update_data = block_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(block, field, value)
    
    db.commit()
    db.refresh(block)
    
    logger.info(f"Block updated: {block.title} (ID: {block.id})")
    
    return BlockResponse.from_orm(block)

@router.delete("/{flow_id}/blocks/{block_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_block(
    flow_id: int,
    block_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить блок"""
    
    user_id = int(current_user["sub"])
    
    block = db.query(Block).filter(
        Block.id == block_id,
        Block.flow_id == flow_id
    ).first()
    
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Block not found"
        )
    
    # Проверяем доступ
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    bot = db.query(Bot).filter(
        Bot.id == flow.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(block)
    db.commit()
    
    logger.info(f"Block deleted: {block.title} (ID: {block.id})")
    
    return None

# ============ CONNECTIONS ============

@router.post("/{flow_id}/connections", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
async def create_connection(
    flow_id: int,
    connection_data: ConnectionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать связь между блоками"""
    
    user_id = int(current_user["sub"])
    
    # Проверяем доступ
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    bot = db.query(Bot).filter(
        Bot.id == flow.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Создаем связь
    connection = Connection(
        from_block_id=connection_data.from_block_id,
        to_block_id=connection_data.to_block_id,
        label=connection_data.label
    )
    
    db.add(connection)
    db.commit()
    db.refresh(connection)
    
    logger.info(f"Connection created: {connection.from_block_id} -> {connection.to_block_id}")
    
    return ConnectionResponse.from_orm(connection)

@router.get("/{flow_id}/connections", response_model=List[ConnectionResponse])
async def get_connections(
    flow_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить все связи flow"""
    
    user_id = int(current_user["sub"])
    
    # Проверяем доступ
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    bot = db.query(Bot).filter(
        Bot.id == flow.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Получаем все блоки flow
    block_ids = [block.id for block in db.query(Block.id).filter(Block.flow_id == flow_id).all()]
    
    # Получаем связи
    connections = db.query(Connection).filter(
        Connection.from_block_id.in_(block_ids)
    ).all()
    
    return [ConnectionResponse.from_orm(conn) for conn in connections]

@router.delete("/{flow_id}/connections/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connection(
    flow_id: int,
    connection_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить связь"""
    
    user_id = int(current_user["sub"])
    
    connection = db.query(Connection).filter(Connection.id == connection_id).first()
    
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )
    
    # Проверяем доступ
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    bot = db.query(Bot).filter(
        Bot.id == flow.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(connection)
    db.commit()
    
    logger.info(f"Connection deleted: ID {connection_id}")
    
    return None
