from typing import Optional
from beanie import Document
from datetime import datetime
from pydantic import Field
import uuid
from pydantic import BaseModel

__all__ = ["Task", "TaskCreate"]


class Task(Document):
    engineer_id: Optional[int] = None
    professor_id: int
    description: str
    task_name: str
    task_id: int = Field(default_factory=lambda: uuid.uuid4().int & (1 << 63) - 1)
    started: bool = False
    started_at: Optional[datetime] = None
    started_by: Optional[str] = None
    completed: bool = False
    completed_at: Optional[datetime] = None
    completed_by: Optional[str] = None
    created_at: datetime = datetime.now()
    deadline: Optional[str] = None


class TaskCreate(BaseModel):
    engineer_id: int
    professor_id: int
    description: str
    task_name: str
