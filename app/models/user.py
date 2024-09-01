from typing import Optional
from pydantic import BaseModel, Field
from schemas.base_entity import TaskStatus, TaskPriority
from datetime import datetime
from uuid import UUID

class SearchUserModel():
    def __init__(self, email, username, priority, first_name, last_name, is_active, page, size) -> None:
        self.email = email
        self.username = username
        self.priority = priority
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.page = page
        self.size = size

class CreateUserModel(BaseModel):
    email = str
    username: str
    hashed_password: str
    first_name = str
    last_name: str
    is_active: bool = True 
    is_admin: bool = False
    company_id: UUID
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "email@gmail.com",
                "username": "sample",
                "hashed_password": "123456",
                "first_name": "Your first name",
                "last_name": "Your last name",
                "is_active": True,
                "is_admin": False,
                "company_id": 1,
            }
        }


class ViewUserModel(BaseModel):
    id: UUID 
    email = str
    username: str
    first_name = str
    last_name: str
    is_active: bool
    company_id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True