from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
import uuid

router = APIRouter()

# Упрощенные модели
class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, Any]
    data: Optional[Dict[str, Any]] = {}

class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None

class Flow(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    name: str = "Untitled Flow"

class FlowSave(BaseModel):
    bot_id: int
    flow: Flow
    flow_id: Optional[str] = None  # Для обновления существующего

# Новая структура: {bot_id: {flow_id: {flow, name, is_active, created_at, updated_at}}}
flows_storage = {}

@router.post("/flows/save")
async def save_flow(flow_data: FlowSave):
    print(f"Received data: {flow_data}")
    bot_id = flow_data.bot_id
    flow_id = flow_data.flow_id or str(uuid.uuid4())
    
    # Инициализируем хранилище для бота если его нет
    if bot_id not in flows_storage:
        flows_storage[bot_id] = {}
    
    # Если это первый flow для бота - делаем его активным
    is_active = len(flows_storage[bot_id]) == 0
    
    flows_storage[bot_id][flow_id] = {
        "flow": flow_data.flow.dict(),
        "flow_id": flow_id,
        "name": flow_data.flow.name,
        "is_active": is_active,
        "created_at": flows_storage[bot_id].get(flow_id, {}).get("created_at", datetime.now().isoformat()),
        "updated_at": datetime.now().isoformat()
    }

    return {
        "success": True,
        "message": "Flow saved successfully",
        "bot_id": bot_id,
        "flow_id": flow_id
    }

@router.get("/flows/{bot_id}")
async def list_bot_flows(bot_id: int):
    """Получить список всех flows для бота"""
    if bot_id not in flows_storage:
        return {"flows": []}
    
    flows_list = [
        {
            "flow_id": flow_id,
            "name": data["name"],
            "is_active": data["is_active"],
            "created_at": data["created_at"],
            "updated_at": data["updated_at"]
        }
        for flow_id, data in flows_storage[bot_id].items()
    ]
    
    return {"flows": flows_list}

@router.get("/flows/{bot_id}/{flow_id}")
async def get_flow(bot_id: int, flow_id: str):
    """Получить конкретный flow"""
    if bot_id not in flows_storage or flow_id not in flows_storage[bot_id]:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    return flows_storage[bot_id][flow_id]

@router.delete("/flows/{bot_id}/{flow_id}")
async def delete_flow(bot_id: int, flow_id: str):
    """Удалить flow"""
    if bot_id not in flows_storage or flow_id not in flows_storage[bot_id]:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    del flows_storage[bot_id][flow_id]
    
    return {"success": True, "message": "Flow deleted"}

@router.put("/flows/{bot_id}/{flow_id}/activate")
async def activate_flow(bot_id: int, flow_id: str):
    """Сделать flow активным"""
    if bot_id not in flows_storage or flow_id not in flows_storage[bot_id]:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    # Деактивируем все flows
    for fid in flows_storage[bot_id]:
        flows_storage[bot_id][fid]["is_active"] = False
    
    # Активируем выбранный
    flows_storage[bot_id][flow_id]["is_active"] = True
    
    return {"success": True, "message": "Flow activated"}
