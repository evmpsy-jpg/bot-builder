from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

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

flows_storage = {}

@router.post("/flows/save")
async def save_flow(flow_data: FlowSave):
    print(f"Received data: {flow_data}")
    bot_id = flow_data.bot_id
    
    flows_storage[bot_id] = {
        "flow": flow_data.flow.dict(),
        "updated_at": datetime.now().isoformat()
    }
    
    return {
        "success": True,
        "message": "Flow saved successfully",
        "bot_id": bot_id
    }

@router.get("/flows/{bot_id}")
async def get_flow(bot_id: int):
    if bot_id not in flows_storage:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    return flows_storage[bot_id]

@router.get("/flows")
async def list_flows():
    return {
        "flows": [
            {"bot_id": bot_id, **data}
            for bot_id, data in flows_storage.items()
        ]
    }

@router.delete("/flows/{bot_id}")
async def delete_flow(bot_id: int):
    if bot_id not in flows_storage:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    del flows_storage[bot_id]
    return {"success": True, "message": "Flow deleted"}