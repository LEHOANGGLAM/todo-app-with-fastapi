from typing import Optional
from pydantic import BaseModel, Field
from schemas.base_entity import TaskStatus, TaskPriority
from datetime import datetime
from models import ViewUserModel
from uuid import UUID

class SearchTaskModel():
    def __init__(self, summary, status, priority, page, size) -> None:
        self.summary = summary
        self.status = status
        self.priority = priority
        self.page = page
        self.size = size

class CreateTaskModel(BaseModel):
    summary: str
    description: Optional[str]
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.MINOR)
    user_id: Optional[UUID] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Task 1",
                "description": "Description for Task 1",
                "status": "TODO",
                "priority": "MINOR",
                "user_id": None,
            }
        }


class ViewTaskModel(BaseModel):
    id: UUID 
    summary: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    user_id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    user: ViewUserModel | None = None
    
    class Config:
        from_attributes = True