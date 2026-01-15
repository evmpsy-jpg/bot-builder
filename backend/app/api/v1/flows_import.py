from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.bot import Bot
from app.models.flow import Flow
from app.models.block import Block
from app.models.connection import Connection

router = APIRouter()


class BlockImport(BaseModel):
    title: str
    type: str
    content: Dict[str, Any]
    position_x: Optional[float] = 0
    position_y: Optional[float] = 0


class ConnectionImport(BaseModel):
    from_index: int  # индекс блока в массиве blocks
    to_index: int


class FlowImport(BaseModel):
    bot_id: int
    name: str
    description: Optional[str] = None
    is_active: bool = True
    blocks: List[BlockImport]
    connections: List[ConnectionImport]


class FlowExport(BaseModel):
    id: int
    bot_id: int
    name: str
    description: Optional[str]
    is_active: bool
    blocks: List[Dict[str, Any]]
    connections: List[Dict[str, Any]]


@router.post("/flows/import", status_code=status.HTTP_201_CREATED)
def import_flow(
    flow_data: FlowImport,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Импорт Flow со всеми блоками и связями одним запросом
    """
    # Получаем user_id из токена
    user_id = int(current_user["sub"])
    
    # Проверка что бот принадлежит пользователю
    bot = db.query(Bot).filter(
        Bot.id == flow_data.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    
    # Создаем Flow
    new_flow = Flow(
        bot_id=flow_data.bot_id,
        name=flow_data.name,
        description=flow_data.description,
        is_active=flow_data.is_active
    )
    db.add(new_flow)
    db.commit()
    db.refresh(new_flow)
    
    # Создаем блоки и сохраняем их ID
    created_blocks = []
    for block_data in flow_data.blocks:
        new_block = Block(
            flow_id=new_flow.id,
            title=block_data.title,
            type=block_data.type,
            content=block_data.content,
            position_x=block_data.position_x,
            position_y=block_data.position_y
        )
        db.add(new_block)
        db.commit()
        db.refresh(new_block)
        created_blocks.append(new_block)
    
    # Создаем связи используя индексы
    created_connections = []
    for conn_data in flow_data.connections:
        if conn_data.from_index >= len(created_blocks) or conn_data.to_index >= len(created_blocks):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid block index in connections"
            )
        
        new_connection = Connection(
            from_block_id=created_blocks[conn_data.from_index].id,
            to_block_id=created_blocks[conn_data.to_index].id
        )
        db.add(new_connection)
        db.commit()
        db.refresh(new_connection)
        created_connections.append(new_connection)
    
    return {
        "flow_id": new_flow.id,
        "name": new_flow.name,
        "blocks_created": len(created_blocks),
        "connections_created": len(created_connections),
        "message": "Flow imported successfully"
    }


@router.get("/flows/{flow_id}/export", response_model=FlowExport)
def export_flow(
    flow_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Экспорт Flow со всеми блоками и связями
    """
    # Получаем user_id из токена
    user_id = int(current_user["sub"])
    
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    # Проверка владельца
    bot = db.query(Bot).filter(
        Bot.id == flow.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Получаем блоки
    blocks = db.query(Block).filter(Block.flow_id == flow_id).all()
    
    # Получаем связи
    connections = db.query(Connection).filter(Connection.flow_id == flow_id).all()
    
    # Формируем ответ
    blocks_data = [
        {
            "id": block.id,
            "title": block.title,
            "type": block.type,
            "content": block.content,
            "position_x": block.position_x,
            "position_y": block.position_y
        }
        for block in blocks
    ]
    
    connections_data = [
        {
            "id": conn.id,
            "from_block_id": conn.from_block_id,
            "to_block_id": conn.to_block_id
        }
        for conn in connections
    ]
    
    return {
        "id": flow.id,
        "bot_id": flow.bot_id,
        "name": flow.name,
        "description": flow.description,
        "is_active": flow.is_active,
        "blocks": blocks_data,
        "connections": connections_data
    }
