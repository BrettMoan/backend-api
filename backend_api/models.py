from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, str]] = None
    deleted: Optional[bool] = False
    deleted_at: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, str]] = None
    deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None
