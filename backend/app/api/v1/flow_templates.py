from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
import json
import os

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.bot import Bot
from app.models.flow import Flow
from app.models.block import Block
from app.models.connection import Connection

router = APIRouter()

# Путь к файлу с шаблонами
TEMPLATES_FILE = os.path.join(
    os.path.dirname(__file__), 
    "../../templates/flows/templates.json"
)


class TemplateInfo(BaseModel):
    """Информация о шаблоне"""
    id: str
    name: str
    description: str
    category: str
    blocks_count: int
    connections_count: int


class TemplateDetail(BaseModel):
    """Детальная информация о шаблоне"""
    id: str
    name: str
    description: str
    category: str
    blocks: List[Dict[str, Any]]
    connections: List[Dict[str, Any]]


class CreateFromTemplate(BaseModel):
    """Запрос на создание Flow из шаблона"""
    bot_id: int
    template_id: str
    flow_name: str = None  # Если не указано, берется из шаблона


def load_templates() -> Dict[str, Any]:
    """Загрузить шаблоны из JSON файла"""
    try:
        with open(TEMPLATES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Templates file not found"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid templates file format"
        )


@router.get("/flow-templates", response_model=List[TemplateInfo])
def get_templates():
    """
    Получить список всех доступных шаблонов
    """
    templates = load_templates()
    
    result = []
    for template_id, template_data in templates.items():
        result.append(TemplateInfo(
            id=template_data["id"],
            name=template_data["name"],
            description=template_data["description"],
            category=template_data["category"],
            blocks_count=len(template_data["blocks"]),
            connections_count=len(template_data["connections"])
        ))
    
    return result


@router.get("/flow-templates/{template_id}", response_model=TemplateDetail)
def get_template_detail(template_id: str):
    """
    Получить детальную информацию о шаблоне
    """
    templates = load_templates()
    
    if template_id not in templates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_id}' not found"
        )
    
    template = templates[template_id]
    
    return TemplateDetail(
        id=template["id"],
        name=template["name"],
        description=template["description"],
        category=template["category"],
        blocks=template["blocks"],
        connections=template["connections"]
    )


@router.post("/flows/from-template", status_code=status.HTTP_201_CREATED)
def create_flow_from_template(
    data: CreateFromTemplate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Создать Flow из шаблона
    """
    # Получаем user_id из токена
    user_id = int(current_user["sub"])
    
    # Проверка что бот принадлежит пользователю
    bot = db.query(Bot).filter(
        Bot.id == data.bot_id,
        Bot.user_id == user_id
    ).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    
    # Загружаем шаблон
    templates = load_templates()
    
    if data.template_id not in templates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{data.template_id}' not found"
        )
    
    template = templates[data.template_id]
    
    # Создаем Flow
    flow_name = data.flow_name if data.flow_name else template["name"]
    
    new_flow = Flow(
        bot_id=data.bot_id,
        name=flow_name,
        description=template["description"],
        is_active=True
    )
    db.add(new_flow)
    db.commit()
    db.refresh(new_flow)
    
    # Создаем блоки
    created_blocks = []
    for block_data in template["blocks"]:
        new_block = Block(
            flow_id=new_flow.id,
            title=block_data["title"],
            type=block_data["type"],
            content=block_data["content"],
            position_x=block_data.get("position_x", 0),
            position_y=block_data.get("position_y", 0)
        )
        db.add(new_block)
        db.commit()
        db.refresh(new_block)
        created_blocks.append(new_block)
    
    # Создаем связи
    created_connections = []
    for conn_data in template["connections"]:
        if conn_data["from_index"] >= len(created_blocks) or conn_data["to_index"] >= len(created_blocks):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid block index in template connections"
            )
        
        new_connection = Connection(
            from_block_id=created_blocks[conn_data["from_index"]].id,
            to_block_id=created_blocks[conn_data["to_index"]].id
        )
        db.add(new_connection)
        db.commit()
        db.refresh(new_connection)
        created_connections.append(new_connection)
    
    return {
        "flow_id": new_flow.id,
        "name": new_flow.name,
        "template_id": data.template_id,
        "blocks_created": len(created_blocks),
        "connections_created": len(created_connections),
        "message": f"Flow created from template '{template['name']}'"
    }
