from sqlalchemy import Column, Uuid, Time
import enum
import uuid

class CompanyMode(enum.Enum):
    UNKNOWN = "UNKNOWN"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DISSOLVED = "DISSOLVED"
    BANKRUPT = "BANKRUPT"
    MERGED = "MERGED"
    
class TaskStatus(enum.Enum):
    DONE = "DONE"
    IN_PROCESS = "IN_PROCESS"
    IN_REVIEW = "IN_REVIEW"
    TODO = "TODO"
    
class TaskPriority(enum.Enum):
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"

class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(Time, nullable=False)
    updated_at = Column(Time, nullable=False)
    