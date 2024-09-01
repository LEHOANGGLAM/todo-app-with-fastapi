from database import Base
from sqlalchemy import Column, String, Enum, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity, TaskStatus, TaskPriority

class Task(Base, BaseEntity):
    __tablename__ = "tasks"

    summary = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    priority = Column(Enum(TaskPriority), nullable=True)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=True)
    
    user = relationship("User")