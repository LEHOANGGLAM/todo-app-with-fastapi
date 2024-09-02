from typing import Optional
from pydantic import BaseModel, Field
from schemas.base_entity import CompanyMode
from datetime import datetime
from uuid import UUID

class SearchCompanyModel():
    def __init__(self, name, mode, page, size) -> None:
        self.name = name
        self.mode = mode
        self.page = page
        self.size = size

class CreateCompanyModel(BaseModel):
    name: str
    description: Optional[str]
    rating: int = Field(ge=0, le=5, default=0)
    mode: CompanyMode = Field(default=CompanyMode.ACTIVE)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Company 1",
                "description": "Description for Company 1",
                "rating": 4,
                "mode": "ACTIVE",
            }
        }

class ViewCompanyModel(BaseModel):
    id: UUID 
    name: str 
    description: Optional[str] = None
    mode: CompanyMode
    rating: int
    created_at: datetime 
    updated_at: datetime 
    
    class Config:
        from_attributes = True
        